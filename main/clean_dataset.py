from PIL import Image, ImageChops
import time
import os
import shutil
import random
import sys

path = "F://lfw-deepfunneled"
move_to = "F://faces_in_wild"


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
    n_images = len(image_paths)
    print(n_images)
    for i in range(len(image_paths)):
        if is_grayscale(os.path.join(folder_path, image_paths[i])):
            os.remove(os.path.join(folder_path, image_paths[i]))
            n_removed_imgs += 1
            print(str(n_removed_imgs) + " | " + str(100 * i / n_images) + " %")


def split_folder(folder_path, move_to_path, n_parts):
    image_paths = os.listdir(folder_path)
    print(len(image_paths))
    n_files_to_move = int(len(image_paths) / n_parts)
    for i in range(n_files_to_move):
        shutil.move(os.path.join(folder_path, image_paths[i]), os.path.join(move_to_path, image_paths[i]))
        print(str(100 * i / n_files_to_move) + " %")


def shuffle_dataset(folder_path):
    image_paths = os.listdir(folder_path)
    random.shuffle(image_paths)
    for i in range(len(image_paths)):
        os.rename(os.path.join(folder_path, image_paths[i]), os.path.join(folder_path, "0" + str(i) + ".jpg"))


def restructure_dataset(folder_path, destination_path):
    subdirectories = [x for x in os.walk(folder_path)]
    print(len(subdirectories))
    counter = 1
    for x in subdirectories:
        if not x[1]:
            images = os.listdir(x[0])
            print(x[0])
            for i in images:
                os.rename(os.path.join(x[0], i), os.path.join(destination_path, str(counter) + ".jpg"))
                counter += 1
    print(counter)


start_time = time.time()
# remove_grayscale(path)
# split_folder(path, move_to, 26)
# remove_grayscale(move_to)
# restructure_dataset(path, move_to)
shuffle_dataset(move_to)
print(str(time.time() - start_time))
