from PIL import Image, ImageChops
from os.path import basename
import time
import os
import shutil
import random
import zipfile
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
    subdirectories = [x for x in os.walk(folder_path) if x[2]]
    image_paths = []
    for r, d, i in subdirectories:
        for image in i:
            image_paths.append(os.path.join(r, image))
        print(str(r))
        print(len(i))
    n_removed_imgs = 0
    n_images = len(image_paths)
    print(n_images)
    for i in range(len(image_paths)):
        if is_grayscale(image_paths[i]):
            os.remove(image_paths[i])
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


def crop_dataset(folder_path, crop_width, crop_height):
    subdirectories = [x for x in os.walk(folder_path) if x[2]]
    image_paths = []
    n_extras = 0
    n_removed = 0
    for r, d, i in subdirectories:
        for image in i:
            image_paths.append(os.path.join(r, image))
        print(str(r))
        print(len(i))
    for i in range(len(image_paths)):
        print(str(n_removed) + " | " + str(n_extras) + " | " + str(100*i/len(image_paths)) + " %")
        img = Image.open(image_paths[i])
        img_width, img_height = img.size
        if img_width < crop_width or img_height < crop_height:
            img.close()
            os.remove(image_paths[i])
            n_removed += 1
            continue
        if img_width > crop_width or img_height > crop_height:
            n_width_crops = 1
            while (n_width_crops + 1) * crop_width <= img_width:
                n_width_crops += 1
            n_height_crops = 1
            while (n_height_crops + 1) * crop_height <= img_height:
                n_height_crops += 1
            img_left = int((img_width - crop_width * n_width_crops) / 2)
            img_top = int((img_height - crop_height * n_height_crops) / 2)
            n_crop = 0
            for x in range(n_height_crops):
                for y in range(n_width_crops):
                    n_crop += 1
                    name = basename(image_paths[i])
                    if n_crop > 1:
                        name = os.path.splitext(basename(image_paths[i]))[0] + "_" + str(n_crop) + ".jpg"
                        n_extras += 1
                    img.crop((img_left + x * crop_width, img_top + y * crop_height, img_left + (x + 1) * crop_width, img_top + (y + 1) * crop_height)).save(os.path.join(os.path.dirname(image_paths[i]), str(name)))
        img.close()
    print("----------------------------")
    print("n_original_images: " + str(len(image_paths)))
    print("n_extra_images: " + str(n_extras))
    print("% increase: " + str(100 * n_extras / len(image_paths)))
    print("current_number_of_images: " + str(n_extras + len(image_paths)))


def create_image_bundle(folder_path, destination_path, bundle_size):
    subdirectories = [x for x in os.walk(folder_path) if x[2]]
    image_paths = []
    for r, d, i in subdirectories:
        for image in i:
            image_paths.append(os.path.join(r, image))
        print(str(d))
    random.shuffle(image_paths)
    bundle = zipfile.ZipFile(destination_path, "w")
    for i in range(min(bundle_size, len(image_paths))):
        print(i)
        bundle.write(image_paths[i], basename(image_paths[i]))
        os.remove(image_paths[i])
    bundle.close()


start_time = time.time()
# remove_grayscale(path)
# split_folder(path, move_to, 26)
# remove_grayscale(move_to)
# restructure_dataset(path, move_to)
# shuffle_dataset(move_to)
crop_dataset("C://Users//Jaroslav Urban//Desktop//ILSVRC2012_img_train", 256, 256)
# remove_grayscale("C://Users//Jaroslav Urban//Desktop//ILSVRC2012_img_train")
# create_image_bundle("C://Users//Jaroslav Urban//Desktop//test", "C://Users//Jaroslav Urban//Desktop//test.zip", 2)
print(str(time.time() - start_time))
