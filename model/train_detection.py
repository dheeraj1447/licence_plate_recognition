import os
import re

import cv2
from pytesseract import pytesseract, Output

from model.image_utils import get_grayscale, thresholding, opening, canny_edge, blur


def train(image_path):
    image = cv2.imread(image_path)
    # '''
    # Cropping the image
    # '''
    # image = image[35:105, 0:450]
    gray = get_grayscale(image)
    blurry = blur(gray)
    thresh = thresholding(blurry)
    open_img = opening(thresh)
    can = canny_edge(open_img)

    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    print(d.keys())

    date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            if re.match(date_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', can)
    cv2.waitKey(0)
