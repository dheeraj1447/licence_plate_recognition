# Loading the required python modules
import pytesseract
import matplotlib.pyplot as plt
import cv2
import glob
import os

path_for_license_plates = os.getcwd() + "/dataset/ALABAMA/*.jpg"
actual_list = []
predicted_license_plates = []

for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):
    license_plate_file = path_to_license_plate.split("/")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)
    actual_list.append(license_plate)

    ''' 
    Read each license plate image file using openCV 
    '''
    img = cv2.imread(path_to_license_plate)

    '''
    Cropping the image
    '''
    cropped_image = img[35:95, 0:450]

    # plt.subplot(3, 3, int(license_plate))
    # plt.imshow(cropped_image)
    # plt.axis('off')

    # plt.imshow(crop)

    '''
    Re-size the image
    '''
    resize_test_license_plate = cv2.resize(
        cropped_image, None, fx=2, fy=2,
        interpolation=cv2.INTER_CUBIC)

    # plt.imshow(resize_test_license_plate)
    # plt.axis('off')
    # plt.title('GWT2180 license plate')

    '''
    Apply grayscale
    '''
    grayscale_resize_test_license_plate = cv2.cvtColor(
        resize_test_license_plate, cv2.COLOR_BGR2GRAY)

    '''
    Apply gaussian blur
    '''
    gaussian_blur_license_plate = cv2.GaussianBlur(
        grayscale_resize_test_license_plate, (5, 5), 0)

    plt.subplot(3, 3, int(license_plate))
    plt.imshow(gaussian_blur_license_plate)
    plt.axis('off')

    ''' 
    We then pass each license plate image file 
    to the Tesseract OCR engine using the Python library  
    wrapper for it. We get back predicted_result for  
    license plate. We append the predicted_result in a 
    list and compare it with the original the license plate 
    '''
    predicted_result = pytesseract.image_to_string(gaussian_blur_license_plate, lang='eng',
                                                   config='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
    predicted_license_plates.append(filter_predicted_result)

plt.show()
print("Actual plate", "Predicted License Plate")
print("------------", "-----------------------")


def list_predicted_plates(actual_list, predicted_list):
    for actual_plate, predict_plate in zip(actual_list, predicted_list):
        print(actual_plate, "\t\t\t", predict_plate)


list_predicted_plates(actual_list, predicted_license_plates)
