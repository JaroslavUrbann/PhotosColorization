from PIL import Image, ImageFile
import os
import time
from skimage.color import rgb2lab, lab2rgb
import numpy as np
from skimage.transform import resize
from keras import layers
from keras import backend as K
from keras.models import model_from_json
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Model:
    def __init__(self):
        self.grayscale_images = []
        self.colorized_images = []
        self.last_image_set_time = time.time()
        self.model = None
        self.pspnet = None
        self.is_colorized = False
        self.cancel = False

    def get_last_grayscale(self):
        if self.grayscale_images:
            return self.grayscale_images[-1]

    def get_last_colorized(self):
        if self.colorized_images and self.is_colorized:
            self.is_colorized = False
            return self.colorized_images[-1]

    def get_colorized_name(self, index):
        return self.colorized_images[index].filename

    # save image
    def save(self, path, name, index):
        if name:
            try:
                self.colorized_images[index].save(os.path.join(path, name), format="jpeg")
            except Exception as e:
                try:
                    self.colorized_images[index].save(os.path.join(path, self.colorized_images[index].filename), format="jpeg")
                except:
                    return False
        else:
            try:
                self.colorized_images[index].save(os.path.join(path, self.colorized_images[index].filename), format="jpeg")
            except:
                return False
        return True

    # save all images
    def save_all(self, path):
        try:
            for i in range(len(self.colorized_images)):
                self.colorized_images[i].save(os.path.join(path, self.colorized_images[i].filename), format="jpeg")
        except:
            return False
        return True

    # loads images to pillow format
    def load_images(self, path: str):
        replaced = False
        try:
            img = Image.open(path)
            filename = img.filename
            img = img.convert("RGB")
            # loses filename attribute for some reason
            img.filename = filename
        except:
            return False, False
        if time.time() - self.last_image_set_time > 0.5:
            self.grayscale_images = []
            replaced = True
        self.grayscale_images.append(img)
        self.last_image_set_time = time.time()
        return True, replaced

    # resizes and converts to grayscale
    def resize_img(self, img):
        w, h = img.size
        if w * h > 1920 * 1080:
            w = 1920 * 1080 / img.size[1]
            h = 1920 * 1080 / img.size[0]
        while int(w) % 8 != 0:
            w += 1
        while int(h) % 8 != 0:
            h += 1
        return img.resize((int(w), int(h))).convert("L").convert("RGB")

    # loads pspnet and main model
    def load_models(self, base_path):
        tim = time.time()
        K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)))
        with open(os.path.join(base_path, "models/pspnet.json")) as pspnet_architecture:
            json_string = pspnet_architecture.read()
        pspnet = model_from_json(json_string, custom_objects={'Interp': Interp})
        pspnet.load_weights(os.path.join(base_path, "models/pspnet.h5"))
        pspnet._make_predict_function()
        self.pspnet = pspnet

        with open(os.path.join(base_path, "models/model.json")) as model_architecture:
            json_string = model_architecture.read()
        model = model_from_json(json_string)
        model.load_weights(os.path.join(base_path, "models/model.h5"))
        model._make_predict_function()
        self.model = model

    # main prediction function
    def start_conversion(self):
        self.cancel = False
        tim = time.time()
        while not self.pspnet or not self.model:
            time.sleep(1)
        if self.cancel:
            return
        self.colorized_images = []
        while len(self.grayscale_images) > len(self.colorized_images) and not self.cancel:
            tim = time.time()
            img = self.resize_img(self.grayscale_images[len(self.colorized_images)])
            segmentation = self.predict_segmentation(img.copy(), (img.size[1] / 8, img.size[0] / 8))
            if self.cancel:
                return
            l = self.img2l(img)
            y = self.model.predict([l, segmentation])
            if self.cancel:
                return
            a, b = np.split(y[0], [1], 2)
            l = l[0, :, :, 0] * 100
            a = (a[:, :, 0] + 1) * 255 / 2 - 127
            b = (b[:, :, 0] + 1) * 255 / 2 - 128
            color_img = np.zeros((l.shape[0], l.shape[1], 3))
            color_img[:, :, 0] = l
            color_img[:, :, 1] = a
            color_img[:, :, 2] = b
            color_img = Image.fromarray((lab2rgb(color_img)*255).astype('uint8'))
            color_img = color_img.resize(self.grayscale_images[len(self.colorized_images)].size)
            # changes images filename to the coresponding grayscale images filename and adds _colorized - for saving image later
            color_img.filename = os.path.splitext(os.path.basename(self.grayscale_images[len(self.colorized_images)].filename))[0] + "_colorized.jpg"
            self.colorized_images.append(color_img)
            self.is_colorized = True

    # converts image to lab
    def img2l(self, img):
        img = rgb2lab(img)
        l = img[:, :, 0]
        l = np.array(l) / 100
        l = np.expand_dims(l, axis=2)
        l = np.expand_dims(l, axis=0)
        return l

    # predicts segmentation with pspnet
    def predict_segmentation(self, img, output_shape):   # w x h
        input_size = 473
        img.thumbnail((input_size, input_size))
        new_img = Image.new('RGB', (input_size, input_size))
        left = int((input_size - img.size[0]) / 2)
        top = int((input_size - img.size[1]) / 2)
        new_img.paste(img, (left, top))
        new_img = np.array(new_img) - np.array([[[128, 128, 128]]])
        segmentation = self.pspnet.predict(np.expand_dims(new_img, axis=0))[:, top:top+img.size[1], left:left+img.size[0], :]
        segmentation = resize(segmentation,
                                (1, output_shape[0], output_shape[1], 150),
                                mode="constant",
                                preserve_range=True)
        return segmentation


# custom pspnet layer
class Interp(layers.Layer):

    def __init__(self, new_size, **kwargs):
        self.new_size = new_size
        super(Interp, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Interp, self).build(input_shape)

    def call(self, inputs, **kwargs):
        new_height, new_width = self.new_size
        resized = K.tf.image.resize_images(inputs, [new_height, new_width],
                                          align_corners=True)
        return resized

    def compute_output_shape(self, input_shape):
        return tuple([None, self.new_size[0], self.new_size[1], input_shape[3]])

    def get_config(self):
        config = super(Interp, self).get_config()
        config['new_size'] = self.new_size
        return config
