import zipfile
from PIL import Image
from skimage.color import rgb2lab
from skimage.transform import resize
from keras.models import model_from_json
import numpy as np
import time


def lab_img(img):
    img = img.convert("RGB")
    print(img)
    img = rgb2lab(img) / 255
    l = img[:, :, 0]
    ab = []
    a = img[:, :, 1]
    b = img[:, :, 2]
    ab.append(a)
    ab.append(b)
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


def batch_images(index, batch_size, filepath, image_paths, pspnet_path, pspnet):
    with zipfile.ZipFile(filepath) as myzip:
        x = []
        segmentation_x = []
        y = []
        for image in range(index * batch_size, min(len(image_paths), index * batch_size + batch_size)):
            with myzip.open(image_paths[image]) as img:
                img = Image.open(img)
                cropped_img = crop_img(img, 300, 300)[0]
                x2 = predict_segmentation(cropped_img, pspnet)
                l, ab = lab_img(cropped_img)
                segmentation_x.append(x2)
                x.append(l)
                y.append(ab)
                segmentation_x.append(np.flipud(x2))
                x.append(np.flipud(l))
                y.append(np.flipud(ab))
        return x, segmentation_x, y


def predict_segmentation(img, pspnet):
    # TODO: do this in my model
    DATA_MEAN = np.array([[[123.68, 116.779, 103.939]]])
    image_size = img.size
    input_size = (473, 473)

    if image_size != input_size:
        img = img.resize(input_size)

    # TODO: check if img has 3 layers
    pixel_img = np.array(img)
    pixel_img = pixel_img - DATA_MEAN
    bgr_img = pixel_img[:, :, ::-1]
    start_time = time.time()
    prediction = pspnet.predict(np.expand_dims(bgr_img, 0))[0]
    print("predicting took ", time.time() - start_time, "s to run")

    # controvertial: de-hot encode pspnet output to make space for higher image resolution predicting
    segmented_image = np.argmax(prediction, axis=2)
    if image_size != input_size:
        segmented_image = resize(segmented_image, image_size)
    return segmented_image


def generator_fn(n_images, batch_size, filepath):
    with zipfile.ZipFile(filepath) as myzip:
        image_paths = myzip.infolist()

    pspnet_path = "../PSPNet/weights/pspnet50_ade20k"
    json_path = pspnet_path + ".json"
    h5_path = pspnet_path + ".h5"
    with open(json_path, 'r') as model_file:
        pspnet = model_from_json(model_file.read())
    pspnet.load_weights(h5_path)

    n_iterations = int(n_images / batch_size)
    for i in range(n_iterations):
        x, segmentation_x, y = batch_images(i, batch_size, filepath, image_paths, pspnet_path, pspnet)
        return x, segmentation_x, y


# TODO: try it with multiple images, validate images
generator_fn(1, 1, 'b_probs.zip')

# model.fit_generator(generator_fn(1000, 32, 'b_probs.zip'),
#         samples_per_epoch=10000, nb_epoch=10)
