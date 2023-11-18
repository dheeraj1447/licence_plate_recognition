import os

import cv2
from pytesseract import pytesseract

from model.image_utils import get_grayscale, thresholding

output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/dataset/train_final/"


def train(image_path, directory, file_name):
    image = cv2.imread(image_path)

    gray = get_grayscale(image)
    # blurry = blur(gray)
    threshold = thresholding(gray)

    output_directory = output_dir + directory + "/"
    # Check if the directory exists, and create it if not
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ tessedit_char_blacklist=[],~`/\.)('
    boxes = pytesseract.image_to_boxes(threshold, config=custom_config).splitlines()

    # Extract bounding box coordinates for each letter
    letter_boxes = []
    for box in boxes:
        b = box.split()
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        letter_boxes.append((x, y, w, h))

    if len(letter_boxes) > 0:
        # Calculate a bounding box that encloses all letter bounding boxes
        min_x = min(box[0] for box in letter_boxes)
        min_y = min(box[1] for box in letter_boxes)
        max_x = max(box[0] + box[2] for box in letter_boxes)
        max_y = max(box[1] + box[3] for box in letter_boxes)

        # Crop the image based on the calculated bounding box
        cropped_image = threshold[min_y:max_y, min_x:max_x]

        # d = pytesseract.image_to_data(cropped_image, config=custom_config, output_type=Output.DICT)
        print(file_name)

        cv2.imwrite(output_directory + file_name + ".jpg", cropped_image)
    else:
        print("skipped image - " + directory + file_name + ".jpg")
