import glob
import os

import cv2
import matplotlib.pyplot as plt
import pytesseract
from pytesseract import Output

from model.image_processing import get_grayscale, get_morphology_top_hat, get_morphology_black_hat, get_gaussian_blur, \
    get_adaptive_threshold, find_contours, find_possible_contours, find_characters, draw_rectangles, \
    get_plate_info_and_images, threshold_again, segment_characters

plt.style.use('dark_background')

path_for_license_plates = os.getcwd() + "/dataset/train/ALASKA/001.jpg"
output_dir = os.path.dirname(os.path.abspath(__file__)) + "/dataset/train_final/"

processed_images = 0
total_images = 0
un_processed_images = 0

for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):
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
                processed_images = processed_images + 1

                final = cv2.imread(output_directory + license_plate + ".jpg")
                custom_config = r'--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ tessedit_char_blacklist=[],~`/\.)('
                d = pytesseract.image_to_data(final, config=custom_config, lang="eng", output_type=Output.DICT)
                print(d)
                # print(file_name)
            else:
                un_processed_images = un_processed_images + 1
                print("Unable to find characters - " + directory + "/" + license_plate_file)
    else:
        un_processed_images = un_processed_images + 1
        print("skipping for file - " + directory + "/" + license_plate_file)

    total_images = total_images + 1

print("############################")
print("Total images - " + str(total_images))
print("############################")
print("Processed images - " + str(processed_images))
print("############################")
print("Unprocessed images - " + str(un_processed_images))
print("############################")
