from scripts.model import Model
from io import BytesIO
from PIL import ImageOps


class Controller:
    def __init__(self):
        self.model = Model()

    def load_images(self, path: str):
        is_loaded, is_replaced = self.model.load_images(path)
        return is_loaded, is_replaced

    def get_last_grayscale(self):
        image = self.model.get_last_grayscale()
        w, h = image.size
        b = round(w/64) if w > h else round(h/64)
        image = ImageOps.expand(image, border=int(b))
        img_io = BytesIO()
        image.save(img_io, format="jpeg")
        img_io.seek(0)
        return img_io

    def get_last_colorized(self):
        image = self.model.get_last_colorized()
        w, h = image.size
        b = round(w/64) if w > h else round(h/64)
        image = ImageOps.expand(image, border=int(b))
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
