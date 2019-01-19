from model import Model
from io import BytesIO


class Controller:
    def __init__(self):
        self.model = Model()

    def set_image_paths(self, path: str):
        is_loaded, is_replaced = self.model.set_image_paths(path)
        return is_loaded, is_replaced

    def get_last_grayscale(self):
        image = self.model.get_last_grayscale()
        img_io = BytesIO()
        image.save(img_io, format="jpeg")
        img_io.seek(0)
        return img_io

    def get_last_colorized(self):
        image = self.model.get_last_colorized()
        img_io = BytesIO()
        image.save(img_io, format="jpeg")
        img_io.seek(0)
        return img_io

    def is_colorized(self):
        return bool(self.model.is_colorized)

    def start(self):
        self.model.start_conversion()

    def save(self):
        pass

    def save_all(self):
        pass

    def cancel(self):
        pass
