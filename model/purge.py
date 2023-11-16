# Removes all previous training and log files.
import os
srcdir = 'tesseract/trainfiles'
destdir = 'tesseract/trainoutput'
files = os.listdir(srcdir)

for item in files:
    if not item.endswith(('.jpg', '.box')):
        os.remove(os.path.join(srcdir, item))

files = os.listdir(destdir)
for item in files:
    os.remove(os.path.join(destdir, item))