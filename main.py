import os

import cv2
from matplotlib import pyplot as plt
from pytesseract import pytesseract, Output

from model.image_processing import get_grayscale, get_morphology_top_hat, get_morphology_black_hat, get_gaussian_blur, \
    get_adaptive_threshold, find_contours, find_possible_contours, find_characters, draw_rectangles, \
    get_plate_info_and_images, threshold_again, segment_characters

plt.style.use('dark_background')

output_dir = os.path.dirname(os.path.abspath(__file__)) + "/temp/"


def process_image(path_to_license_plate):
    directory = path_to_license_plate.split("/")[-2]
    license_plate_file = path_to_license_plate.split("/")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)

    original_image = cv2.imread(path_to_license_plate)
    height, width, channel = original_image.shape
    # Grayscale
    gray = get_grayscale(original_image)
    # Morphology TopHat
    imgTopHat = get_morphology_top_hat(gray)
    # Morphology BlackHat
    imgBlackHat = get_morphology_black_hat(gray)
    # Add gray and tophat
    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    # Subtract blackhat from added result
    gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)
    # Apply gaussian blur
    img_blurred = get_gaussian_blur(gray)
    # apply adaptive threshold
    img_thresh = get_adaptive_threshold(img_blurred)
    # find contours
    contours_dict = find_contours(img_thresh, height, width, channel)
    # find possible contours
    possible_contours = find_possible_contours(contours_dict)
    # find characters
    result_idx = find_characters(possible_contours, possible_contours)

    if len(result_idx) > 0:
        # draw rectangles
        original_image, matched_result = draw_rectangles(original_image, result_idx[0], possible_contours)
        # get plate info and images
        plate_info, plate_image = get_plate_info_and_images(matched_result, img_thresh, height, width)
        # Threshold again
        img_threshold = threshold_again(plate_image, license_plate_file)
        if len(img_threshold) > 0:
            # Take negative img
            negative_img = 255 - img_threshold
            # Segment characters
            char = segment_characters(negative_img)

            if len(char) > 0:
                plt.style.use('ggplot')

                for i in range(len(char)):
                    plt.subplot(1, len(char), i + 1)
                    plt.imshow(char[i], cmap='gray')
                    plt.axis('off')

                output_directory = output_dir + directory + "/"
                # Check if the directory exists, and create it if not
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                plt.savefig(output_directory + license_plate + ".jpg", bbox_inches='tight')
                plt.close()

                final = cv2.imread(output_directory + license_plate + ".jpg")
                custom_config = r'--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ tessedit_char_blacklist=[],~`/\.)('
                d = pytesseract.image_to_data(final, config=custom_config, lang="eng", output_type=Output.DICT)
                filtered_list = [element for element in d['text'] if element != ""]
                return filtered_list[0] if len(filtered_list) > 0 else ''
            else:
                print("Unable to find characters - " + directory + "/" + license_plate_file)
    else:
        print("skipping for file - " + directory + "/" + license_plate_file)

