import os
from model.train_detection import train

path_for_license_plates = os.getcwd() + "/dataset/train/ALASKA/002.jpg"

train(path_for_license_plates)
