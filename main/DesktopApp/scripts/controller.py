from scripts.model import Model
from io import BytesIO
from PIL import ImageOps


class Controller:
    def __init__(self):
        self.model = Model()

    def set_image_paths(self, path: str):
        is_loaded, is_replaced = self.model.set_image_paths(path)
        return is_loaded, is_replaced

    def get_last_grayscale(self):
        image = self.model.get_last_grayscale()
        w, h = image.size
        while w > 639 or h > 639:
            w -= 1
            h -= image.size[1] / image.size[0]
        while w < 640 or h < 640:
            w += 1
            h += image.size[1] / image.size[0]
        image = ImageOps.expand(image.resize((int(w), int(h))), border=15)
        img_io = BytesIO()
        image.save(img_io, format="jpeg")
        img_io.seek(0)
        return img_io

    def get_last_colorized(self):
        image = self.model.get_last_colorized()
        w, h = image.size
        while w > 639 or h > 639:
            w -= 1
            h -= image.size[1] / image.size[0]
        while w < 640 or h < 640:
            w += 1
            h += image.size[1] / image.size[0]
        image = ImageOps.expand(image.resize((int(w), int(h))), border=15)
        img_io = BytesIO()
        image.save(img_io, format="jpeg")
        img_io.seek(0)
        return img_io

    def get_colorized_name(self, index):
        return self.model.get_colorized_name(index)

    def is_colorized(self):
        return bool(self.model.is_colorized)

    def load_models(self, base_path):
        self.model.load_models(base_path)

    def start(self):
        self.model.start_conversion()

    def save(self, path, name, index):
        return self.model.save(path, name, index)

    def save_all(self, path):
        return self.model.save_all(path)

    def cancel(self):
        self.model.cancel = True
