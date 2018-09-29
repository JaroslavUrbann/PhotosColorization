from PIL import Image
import glob

#TODO: Guetzli

def split_images(images_path, train_size=0.9):
    image_paths = glob.glob(images_path + "/*.*")
    a = int(len(image_paths)*train_size)
    train_x = image_paths[:a]
    test_x = image_paths[a:len(image_paths)]
    return train_x, test_x


def png2jpg(bytes_img):
    jpg_img = bytes_img.convert("RGB")
    return jpg_img


def resize_img(bytes_img, width, height):
    resized_img = bytes_img.resize((width, height), Image.ANTIALIAS)
    return resized_img