import zipfile
from PIL import Image
from skimage.color import rgb2lab
import numpy as np
from skimage.transform import resize
import tensorflow as tf
import time
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


# Returns batch of x and y values packed together
def batch_images(index, batch_size, image_paths, trained_model, imgs):
    x_batch = []
    s_batch = []
    y_batch = []
    for image in range(index, index + batch_size):
        with imgs.open(image_paths[image]) as img:
            print(image_paths[image])
            img = Image.open(img)

            s = predict_segmentation(img, trained_model)
            l, a, b = lab_img(img)

            y = np.concatenate((a, b), axis=2)

            x_batch.append(l)
            s_batch.append(s)
            y_batch.append(y)

            x = np.fliplr(l)
            s = np.fliplr(s)
            y = np.fliplr(y)

            x_batch.append(x)
            s_batch.append(s)
            y_batch.append(y)

    return x_batch, s_batch, y_batch


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
    start_time = time.time()
    if image_size != input_size:
        segmented_img = resize(segmented_img,
                               (image_size[1], image_size[0], 150),
                                mode="constant")
    print(time.time() - start_time)
    return segmented_img


# Yields batches of x and y values
def generator_fn(n_images, batch_size, images_path, trained_model):
    with zipfile.ZipFile(images_path) as imgs:
        image_paths = imgs.infolist()

        i = 0
        while True:
            if i + batch_size > n_images:
                i = 0
            x, s, y = batch_images(i, batch_size, image_paths, trained_model, imgs)
            i += batch_size
            yield [np.array(x), np.array(s)], np.array(y)
