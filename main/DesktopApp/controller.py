from model import Model
from glob import glob
from PIL import Image
import os
import time


class Controller:
    def __init__(self):
        self.model = Model()

    def set_image_paths(self, path: str):
        is_loaded = self.model.set_image_paths(path)
        return is_loaded

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

    def start(self):
        pass

    def save(self):
        pass

    def save_all(self):
        pass

    def cancel(self):
        pass
