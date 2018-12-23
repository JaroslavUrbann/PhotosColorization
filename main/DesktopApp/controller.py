from model import Model
from glob import glob
from PIL import Image
import os
import time


class Controller:
    def __init__(self):
        self.model = Model()
        self.grayscale_images = []

    def set_image_paths(self, path: str):
        is_loaded = self.model.set_image_paths(path)
        if self.model.images:
            self.grayscale_images = self.model.grayscale_images
        return is_loaded

    def start(self):
        pass
