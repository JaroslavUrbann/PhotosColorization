import zipfile
from PIL import Image
from skimage.color import rgb2lab
import numpy as np
from scipy import ndimage
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)


# Returns numpy arrays l, a and b (w x h x 1)
def lab_img(img):
    if img.format != ("JPEG" or "JPG"):
        img = img.convert("RGB")
    img = rgb2lab(img)

    l = img[:, :, 0]
    a = img[:, :, 1]
    b = img[:, :, 2]

    l = np.array(l) / 100
    a = (np.array(a) + 127) / 255
    b = (np.array(b) + 128) / 255

    l = np.expand_dims(l, axis=2)
    a = np.expand_dims(a, axis=2)
    b = np.expand_dims(b, axis=2)

    return l, a, b


# Returns array with images made from original image
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


# Returns batch of x and y values packed together
def batch_images(index, batch_size, images_path, image_paths, trained_model):
    with zipfile.ZipFile(images_path) as my_zip:
        x_batch = []
        y_batch = []
        start_position = index * batch_size
        end_position = min(len(image_paths), index * batch_size + batch_size)
        for image in range(start_position, end_position):
            with my_zip.open(image_paths[image]) as img:
                img = Image.open(img)
                segmentation = predict_segmentation(img, trained_model)
                l, a, b = lab_img(img)

                x = np.concatenate((l, segmentation), axis=2)
                y = np.concatenate((a, b), axis=2)

                x_batch.append(x)
                y_batch.append(y)

                # flipped_x2 = np.flipud(x2)
                # flipped_x = np.flipud(l)
                # x.append(np.concatenate((flipped_x, flipped_x2), axis=2))
                # y.append(np.flipud(ab))

        return x_batch, y_batch


# Returns one-hot encoded segmentation object (w x h x 150)
def predict_segmentation(img, trained_model):
    # TODO: do this in my model
    data_mean = np.array([[[123.68, 116.779, 103.939]]])
    image_size = img.size
    input_size = (473, 473)

    if image_size != input_size:
        img = img.resize(input_size)

    pixel_img = np.array(img)
    pixel_img = pixel_img - data_mean
    bgr_img = pixel_img[:, :, ::-1]
    segmented_img = trained_model.predict(np.expand_dims(bgr_img, 0))[0]
    if image_size != input_size:
        segmented_img = ndimage.zoom(segmented_img, (1 * image_size[1] / input_size[1],
                                                     1 * image_size[0] / input_size[0], 1))
    return segmented_img


# Yields batches of x and y values
def generator_fn(n_images, batch_size, images_path, trained_model):
    with zipfile.ZipFile(images_path) as my_zip:
        image_paths = my_zip.infolist()

    batches_per_epoch = int(n_images / batch_size)

    while True:
        for i in range(batches_per_epoch):
            x, y = batch_images(i, batch_size, images_path, image_paths, trained_model)
            yield x, y


# TODO: flipped
