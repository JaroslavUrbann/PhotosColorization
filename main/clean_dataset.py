from PIL import Image, ImageChops
import time
import os
import shutil

path = "F://coco2017_1/"
move_to = "F://coco2017_2/"


def is_grayscale(img_path):
    img = Image.open(img_path)
    if img.mode == "RGB":
        rgb = img.split()
        if ImageChops.difference(rgb[0], rgb[1]).getextrema()[1] != 0:
            return False
        if ImageChops.difference(rgb[0], rgb[2]).getextrema()[1] != 0:
            return False
    return True


def remove_grayscale(folder_path):
    n_removed_imgs = 0
    image_paths = os.listdir(folder_path)
    print(len(image_paths))
    for i in range(len(image_paths)):
        if is_grayscale(folder_path + image_paths[i]):
            os.remove(folder_path + image_paths[i])
            n_removed_imgs += 1
            print(str(n_removed_imgs) + " | " + str(i) + " / " + str(len(image_paths)))


def split_folder(folder_path, move_to_path):
    image_paths = os.listdir(folder_path)
    print(len(image_paths))
    n_files_to_move = int(len(image_paths) / 2)
    for i in range(n_files_to_move):
        shutil.move(folder_path + image_paths[i], move_to_path + image_paths[i])
        print(str(i) + " / " + str(n_files_to_move))


start_time = time.time()
remove_grayscale(path)
print(str(time.time() - start_time))
