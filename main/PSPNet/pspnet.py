#!/usr/bin/env python
from __future__ import print_function
from os.path import splitext, join, isdir, basename
import numpy as np
from scipy import misc, ndimage
from keras import backend as K
from keras.models import model_from_json, load_model
import tensorflow as tf
import layers_builder as l
import utils as u
from keras.utils.generic_utils import CustomObjectScope

# These are the means for the ImageNet pretrained ResNet
DATA_MEAN = np.array([[[123.68, 116.779, 103.939]]])  # RGB order


class PSPNet(object):
    def __init__(self):
        self.input_shape = (473, 473)
        json_path = join("weights", "pspnet50_ade20k" + ".json")
        h5_path = join("weights", "pspnet50_ade20k" + ".h5")
        print("Keras model & weights found, loading...")
        with CustomObjectScope({'Interp': l.Interp}):
            with open(json_path, 'r') as file_handle:
                self.model = model_from_json(file_handle.read())
        self.model.load_weights(h5_path)

    def predict(self, img):

        h_ori, w_ori = img.shape[:2]

        img = misc.imresize(img, self.input_shape)

        img = img - DATA_MEAN
        img = img[:, :, ::-1]  # RGB => BGR
        img = img.astype('float32')
        print("Predicting...")

        probs = self.feed_forward(img)

        if img.shape[0:1] != self.input_shape:  # upscale prediction if necessary
            h, w = probs.shape[:2]
            probs = ndimage.zoom(probs, (1. * h_ori / h, 1. * w_ori / w, 1.),
                                 order=1, prefilter=False)

        print("Finished prediction...")

        return probs

    def feed_forward(self, data):
        assert data.shape == (self.input_shape[0], self.input_shape[1], 3)
        prediction = self.model.predict(np.expand_dims(data, 0))[0]
        return prediction


if __name__ == "__main__":

    input_path = "a.jpg"
    output_path = "b.jpg"
    input_size = 500

    pspnet = PSPNet()

    img = misc.imread(input_path, mode='RGB')
    cimg = misc.imresize(img, (input_size, input_size))

    probs = pspnet.predict(img)

    cm = np.argmax(probs, axis=2)
    pm = np.max(probs, axis=2)

    color_cm = u.add_color(cm)
    print(cm.shape)
    # with open("img.txt", "w") as im:
    #     for i in range(cm.shape[1]):
    #         im.write(' '.join(map(str, cm[i])) + '\n')

    alpha_blended = 0.5 * color_cm * 255 + 0.5 * img

    filename, ext = splitext(output_path)

    misc.imsave(filename + "_seg_read" + ext, cm)
    misc.imsave(filename + "_seg" + ext, color_cm)
    misc.imsave(filename + "_probs" + ext, pm)
    misc.imsave(filename + "_seg_blended" + ext, alpha_blended)
