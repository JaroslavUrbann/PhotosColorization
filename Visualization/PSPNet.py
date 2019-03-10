from keras.models import load_model
from skimage.transform import resize
from keras.backend import tf as ktf
from keras import layers
import os
import numpy as np


class Interp(layers.Layer):

    def __init__(self, new_size, **kwargs):
        self.new_size = new_size
        super(Interp, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Interp, self).build(input_shape)

    def call(self, inputs, **kwargs):
        new_height, new_width = self.new_size
        resized = ktf.image.resize_images(inputs, [new_height, new_width],
                                          align_corners=True)
        return resized

    def compute_output_shape(self, input_shape):
        return tuple([None, self.new_size[0], self.new_size[1], input_shape[3]])

    def get_config(self):
        config = super(Interp, self).get_config()
        config['new_size'] = self.new_size
        return config


def load_pspnet(path):
    trained_model = load_model(path, custom_objects={'Interp': Interp})
    trained_model._make_predict_function()
    return trained_model


def predict_segmentation(img):
    img = img.convert("L").convert("RGB")
    pspnet = load_pspnet("C://Users//Jaroslav Urban//Desktop//PhotosColorization//models//pspnet.h5")
    data_mean = np.array([[[123.68, 116.779, 103.939]]])
    input_size = (473, 473)
    output_size = (img.size[0] / 8, img.size[1] / 8)

    if img.size != input_size:
        img = img.resize(input_size)

    pixel_img = np.array(img)
    pixel_img = pixel_img - data_mean
    bgr_img = pixel_img[:, :, ::-1]
    segmented_img = pspnet.predict(np.expand_dims(bgr_img, 0))
    if output_size != input_size:
          segmented_img = resize(segmented_img,
                                 (1, output_size[1], output_size[0], 150),
                                  mode="constant",
                                  preserve_range=True)
    return segmented_img