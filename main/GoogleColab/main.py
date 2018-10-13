import zipfile
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from keras.models import model_from_json
import numpy as np
import time
from scipy import misc, ndimage
import sys


def lab_img(img):
    if img.format != ("JPEG" or "JPG"):
        img = img.convert("RGB")
    img = rgb2lab(img) / 255
    l = img[:, :, 0]
    ab = []
    a = img[:, :, 1]
    b = img[:, :, 2]
    ab.append(a)
    ab.append(b)
    l = np.array(l)
    ab = np.array(ab)
    return l, ab


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


def batch_images(index, batch_size, file_path, image_paths, psp_net):
    with zipfile.ZipFile(file_path) as my_zip:
        x = []
        segmentation_x = []
        y = []
        start_position = index * batch_size
        end_position = min(len(image_paths), index * batch_size + batch_size)
        for image in range(start_position, end_position):
            with my_zip.open(image_paths[image]) as img:
                img = Image.open(img)
                cropped_img = crop_img(img, 300, 300)[0]
                x2 = predict_segmentation(cropped_img, psp_net)
                l, ab = lab_img(cropped_img)

                segmentation_x.append(x2)
                x.append(l)
                y.append(ab)

                segmentation_x.append(np.flipud(x2))
                x.append(np.flipud(l))
                y.append(np.flipud(ab))

        return x, segmentation_x, y


def predict_segmentation(img, psp_net):
    # TODO: do this in my model
    data_mean = np.array([[[123.68, 116.779, 103.939]]])
    image_size = img.size
    input_size = (473, 473)

    if image_size != input_size:
        img = img.resize(input_size)

    # TODO: check if img has 3 layers
    pixel_img = np.array(img)
    pixel_img = pixel_img - data_mean
    bgr_img = pixel_img[:, :, ::-1]
    start_time = time.time()
    prediction = psp_net.predict(np.expand_dims(bgr_img, 0))[0]
    print("predicting took ", time.time() - start_time, "s to run")

    # controversial: de-hot encode psp_net output to make space for higher image resolution predicting
    segmented_image = np.argmax(prediction, axis=2)
    if image_size != input_size:
        segmented_image = ndimage.zoom(segmented_image,
                                       (1. * image_size[0] / input_size[0],
                                        1. * image_size[1] / input_size[1]),
                                       order=1, prefilter=False)
    segmented_image = (segmented_image - 74.5) / 74.5
    return segmented_image


def generator_fn(n_images, batch_size, file_path):
    with zipfile.ZipFile(file_path) as my_zip:
        image_paths = my_zip.infolist()

    psp_net_path = "../PSPNet/weights/pspnet50_ade20k"
    json_path = psp_net_path + ".json"
    h5_path = psp_net_path + ".h5"
    with open(json_path, 'r') as model_file:
        psp_net = model_from_json(model_file.read())
    psp_net.load_weights(h5_path)

    n_iterations = int(n_images / batch_size)
    for i in range(n_iterations):
        x, segmentation_x, y = batch_images(i, batch_size, file_path, image_paths, psp_net)
        return x, segmentation_x, y


# TODO: colorize segmentation with labels
def decode_images(images):
    w, h = images[0][0].shape
    l = images[0][0]
    a = images[2][0][0]
    b = images[2][1][0]

    semantic_segmentation = np.round(images[1][0] * 74.5 + 74.5)
    misc.imsave("bnw_segmentation.jpg", semantic_segmentation)

    bnw_input = np.zeros((w, h, 3))
    bnw_input[:, :, 0] = l
    misc.imsave("bnw_input.jpg", lab2rgb(bnw_input))

    color_output = np.zeros((w, h, 3))
    color_output[:, :, 0] = 80
    color_output[:, :, 1] = a
    color_output[:, :, 2] = b
    misc.imsave("color_output.jpg", lab2rgb(color_output))


# TODO: try it with multiple images
decode_images(generator_fn(1, 1, 'b_probs.zip'))

# model.fit_generator(generator_fn(1000, 32, 'b_probs.zip'),
#         samples_per_epoch=10000, nb_epoch=10)
