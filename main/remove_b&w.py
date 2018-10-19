from PIL import Image, ImageChops
import zipfile
import time
import os

file_path = "datasetpath"
n_removed_imgs = 0


def is_grayscale(img_path):
    img = Image.open(img_path)
    if img.mode == "RGB":
        rgb = img.split()
        if ImageChops.difference(rgb[0], rgb[1]).getextrema()[1] != 0:
            return False
        if ImageChops.difference(rgb[0], rgb[2]).getextrema()[1] != 0:
            return False
    return True


starttime = time.time()

with zipfile.ZipFile(file_path) as my_zip:
    image_paths = my_zip.infolist()
    for img_path in image_paths:
        if is_grayscale(img_path):
            os.remove(img_path)
            n_removed_imgs += 1
            print(n_removed_imgs)

print(n_removed_imgs)
print(str(time.time() - starttime))
