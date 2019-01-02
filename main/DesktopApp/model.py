from glob import glob
from PIL import Image
import os
import time
from skimage.color import rgb2lab, lab2rgb
import numpy as np
from skimage.transform import resize
from keras.models import load_model
from keras import layers
from keras.backend import tf as ktf


class Model:
    def __init__(self):
        self.grayscale_images = []
        self.colorized_images = []
        self.is_working = False
        self.last_image_set_time = time.time()
        self.model = None
        self.pspnet = None

    def next_grayscale(self, image):
        pass

    def previous_grayscale(self, image):
        pass

    def next_colorized(self, image):
        pass

    def previous_colorized(self, image):
        pass

    def get_progress(self):
        pass

    def set_image_paths(self, path: str):
        image_paths = []
        if not self.is_working:
            if os.path.isdir(path):
                image_paths.extend(glob(os.path.join(path, "*.jpg")))
                image_paths.extend(glob(os.path.join(path, "*.png")))
            else:
                extension = os.path.splitext(path)[1].lower()
                if extension == ".jpg" or extension == ".png":
                    image_paths.append(path)
            if image_paths:
                images = []
                for image_path in image_paths:
                    try:
                        images.append(Image.open(image_path))
                    except:
                        pass
                if time.time() - self.last_image_set_time > 0.1:
                    self.grayscale_images = images
                else:
                    self.grayscale_images.extend(images)
                self.last_image_set_time = time.time()
                return bool(self.grayscale_images)
        return False

    def resize_img(self, img):
        w, h = img.size
        if w * h > 1920 * 1080:
            w = 1920 * 1080 / img.size[1]
            h = 1920 * 1080 / img.size[0]
        while w % 8 != 0:
            w += 1
        while h % 8 != 0:
            h += 1
        return img.resize((w, h)).convert("L").convert("RGB")

    def start_conversion(self):
        if self.is_working or not self.grayscale_images:
            return
        if not self.pspnet:
            self.pspnet = load_model("pspnet.h5", custom_objects={'Interp': Interp})
            self.pspnet._make_predict_function()
        if not self.model:
            self.model = load_model("model_final.hdf5")

        for i in range(len(self.grayscale_images)):
            img = self.resize_img(self.grayscale_images[i])
            l = self.img2l(img)
            segmentation = self.predict_segmentation(img, img.size / 8)
            y = self.model.predict([l, segmentation])
            print(y.shape)
            a, b = np.split(y[0], [1], 2)  # možná líp?
            l = l[:, :, 0] * 100
            a = (a[:, :, 0] + 1) * 255 / 2 - 127
            b = (b[:, :, 0] + 1) * 255 / 2 - 128
            color_img = np.zeros((img.size[1], img.size[0], 3))
            color_img = Image.fromarray((lab2rgb(color_img)*255).astype('uint8'))
            self.colorized_images.append(color_img.resize(self.grayscale_images[i].size))

    def img2l(self, img):
        img = rgb2lab(img)
        l = img[:, :, 0]
        l = np.array(l) / 100
        l = np.expand_dims(l, axis=2)
        l = np.expand_dims(l, axis=0)
        return l

    def predict_segmentation(self, img, output_size):   # w x h
        input_size = 473
        img.thumbnail((input_size, input_size))
        new_img = Image.new('RGB', (input_size, input_size))
        left = int((input_size - img.size[0]) / 2)
        top = int((input_size - img.size[1]) / 2)
        new_img.paste(img, (left, top))
        new_img = np.array(new_img) - np.array([[[123.68, 116.779, 103.939]]])
        bgr_img = new_img[:, :, ::-1]
        segmented_img = self.pspnet.predict(np.expand_dims(bgr_img, axis=0))[:, top:top+img.size[1], left:left+img.size[0], :]
        if output_size != (473, 473):
            segmented_img = resize(segmented_img,
                                   (1, output_size[1], output_size[0], 150),
                                   mode="constant",
                                   preserve_range=True)
        return segmented_img


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
