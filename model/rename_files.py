import os

path_for_license_plates = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/dataset/train/ALABAMA"

images = [f for f in os.listdir(path_for_license_plates) if f.endswith(('.jpg', '.jpeg'))]
print(f"{len(images)} number of images found")
lang = input('Enter The language without spaces\n')
font = input('Enter font without spaces\n')
part1 = f"{lang}.{font}.exp"
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    os.rename(os.path.join(path_for_license_plates, image), os.path.join(path_for_license_plates, filename))