import os

path_for_license_plates = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/dataset/train/ALABAMA"
os.chdir(path_for_license_plates)
number_of_files = len(os.listdir('./'))
for i in range(0, number_of_files):
    os.system(f"tesseract eng.ocrb.exp{i}.jpg eng.ocrb.exp{i} batch.nochop makebox")