import os
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from skimage import io, color
import glob
from PIL import Image

def load_data():
    image_list = map(Image.open, glob(''))