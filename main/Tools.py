from PIL import Image
import glob

# TODO: Guetzli or any other compression. Guetzli takes too long


def split_images(images_path, train_size=0.9):
    image_paths = glob.glob(images_path + "/*.*")
    a = int(len(image_paths)*train_size)
    train_x = image_paths[:a]
    test_x = image_paths[a:len(image_paths)]
    return train_x, test_x


def png2jpg(img):
    if img.format == ("JPEG" or "JPG"):
        return img
    jpg_img = img.convert("RGB")
    return jpg_img


def resize_img(img, width, height):
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    return resized_img


def crop_img(img, crop_width, crop_height):
    img_width, img_height = img.size
    images = []
    x, y = 0, 0
    # TODO: center cropped image(s)
    while img_height >= y + crop_height:
        while img_width >= x + crop_width:
            images.append(img.crop((x, y, x + crop_width, y + crop_height)))
            x = x + crop_width
        x = 0
        y = y + crop_height
    return images


def flip_img(img):
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return flipped_img


# import time
# start = time.time()
# img = Image.open("../datasets/celebA/1172.jpg")

# for a in range(10000):
#     i = png2jpg(img)
# print('It took {0:0.1f} seconds'.format(time.time() - start))

# crop_imgs = crop_img(img, 800, 400)
# for i in range(len(crop_imgs)):
#     crop_imgs[i].save(".../0000000000" + str(i) + ".jpg")
