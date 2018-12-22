from kivy.app import App
from kivy.core.window import Window
from glob import glob
from model import Model
import os
Window.size = (1024, 576)


class PhotosColorizationApp(App):
    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        self.Controller = Controller()
        return

    def on_drop_file(self, window, file_path):
        print(self.Controller.set_image_paths(file_path))
        print(self.Controller.image_paths)
        return


class Controller:
    def __init__(self):
        self.image_paths = []
        self.is_working = False
        self.model = Model()

    def set_image_paths(self, path):
        image_paths = []
        path = str(path, 'UTF-8')
        if not self.is_working:
            if os.path.isdir(path):
                image_paths.extend(glob(os.path.join(path, "*.jpg")))
                image_paths.extend(glob(os.path.join(path, "*.png")))
            else:
                print(os.path.splitext(path)[1])
                if os.path.splitext(path)[1] == (".jpg" or ".png"):
                    image_paths.append(path)
            if image_paths:
                self.image_paths = image_paths
                return True
        return False

    def start(self):
        if not self.is_working:
            pass
        return


PhotosColorizationApp().run()
