from glob import glob
from PIL import Image
import os
import time


class Model:
    def __init__(self):
        self.grayscale_images = []
        self.colorized_images = []
        self.is_working = False
        self.last_image_set_time = time.time()

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

    def start_conversion(self):
        if not self.is_working:
            pass
        return
