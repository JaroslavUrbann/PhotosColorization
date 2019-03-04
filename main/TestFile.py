from PIL import Image, ImageFilter
import numpy as np
from skimage.util import random_noise
from scipy.ndimage.filters import gaussian_filter

im1 = np.asarray(Image.open('2.jpg'))
xd = np.random.normal(0, 5, im1.shape)
xd = im1 + xd
out_array = np.clip(xd, a_min=0, a_max=255)
im = Image.fromarray(np.uint8(gaussian_filter(out_array, sigma=0.5)))
# im1 = im.filter(ImageFilter.GaussianBlur(radius=0.5))
im.save("Y3.jpg")
