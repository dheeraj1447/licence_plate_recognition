import glob
import os
from model.train_detection import train

path_for_license_plates = os.getcwd() + "/dataset/train/**/*.jpg"

for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):
    directory = path_to_license_plate.split("/")[-2]
    license_plate_file = path_to_license_plate.split("/")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)
    train(path_to_license_plate, directory, license_plate)

