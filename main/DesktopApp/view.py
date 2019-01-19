from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from threading import Thread
import controller
import time
from PIL import Image
import os
from glob import glob
Window.size = (1024, 576)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class PhotosColorizationApp(App):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    Controller = controller.Controller()
    grayscale_images = []
    colorized_images = []
    grayscale_index = 0
    colorized_index = 0
    popup = None
    is_working = False

    timer_period = 45
    timer_break = False

    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        self.update_buttons()

    def start_timer(self):
        start = 0
        length = 1000
        start_time = time.time()
        self.timer_break = False
        if self.timer_period == 0:
            try:
                with open("t.txt", "r") as t:
                    self.timer_period = int(str(t.readline()))
            except:
                self.timer_period = 45
        while True:
            if self.root.ids.pb.value < start + length:
                self.root.ids.pb.value += 1

            if self.Controller.is_colorized() or self.timer_break:
                # finishes up the progressbar if it is still not finished and then resets it
                while self.root.ids.pb.value < start + length:
                    self.root.ids.pb.value += 1
                    time.sleep(1 / (length + start - self.root.ids.pb.value))
                self.root.ids.pb.value = start

                if not self.timer_break:
                    self.timer_period = time.time() - start_time
                    with open("t.txt", "w") as t:
                        print("wrote")
                        t.write(str(self.timer_period))
                    self.colorized_images.append(self.Controller.get_last_grayscale())
                    self.colorized_index = len(self.colorized_images) - 1
                    self.colorized_images[self.colorized_index].seek(0)
                    self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index],
                                                                    ext='jpg').texture
                    self.update_buttons()
                if self.timer_break or len(self.colorized_images) >= len(self.grayscale_images):
                    print("breaks")
                    self.is_working = False
                    return
            time.sleep(self.timer_period / length)

    def on_drop_file(self, window, file_path):
        self.upload_images(str(file_path, 'UTF-8'))

    def load(self, path, file_path):
        self.upload_images(file_path[0])
        self.dismiss_popup()

    def upload_images(self, path):
        if not self.is_working:
            image_paths = []
            if os.path.isdir(path):
                image_paths.extend(glob(os.path.join(path, "*.jpg")))
                image_paths.extend(glob(os.path.join(path, "*.png")))
            else:
                extension = os.path.splitext(path)[1].lower()
                if extension == ".jpg" or extension == ".png":
                    image_paths.append(path)
            for p in image_paths:
                is_loaded, is_replaced = self.Controller.set_image_paths(p)
                if is_loaded:
                    if is_replaced:
                        self.grayscale_images = []
                    self.grayscale_images.append(self.Controller.get_last_grayscale())
                    self.grayscale_index = 0
                    self.grayscale_images[self.colorized_index].seek(0)
                    self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index],
                                                                ext='jpg').texture
            self.update_buttons()

    def dismiss_popup(self):
        self.popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self.popup.open()
        self.root.ids.grayscale_img.source = "assets/d.jpg"

    def update_buttons(self):
        self.root.ids.next_grayscale.disabled = len(self.grayscale_images) <= self.grayscale_index + 1
        self.root.ids.previous_grayscale.disabled = self.grayscale_index < 1
        self.root.ids.next_colorized.disabled = len(self.colorized_images) <= self.colorized_index + 1
        self.root.ids.previous_colorized.disabled = self.colorized_index < 1
        self.root.ids.start.disabled = not bool(self.grayscale_images) or self.is_working
        self.root.ids.load.disabled = self.is_working
        self.root.ids.save.disabled = len(self.colorized_images) == 0
        self.root.ids.save_all.disabled = len(self.colorized_images) == 0



    def start(self):
        self.is_working = True
        self.update_buttons()
        timer = Thread(target=self.start_timer)
        timer.daemon = True
        timer.start()
        prediction = Thread(target=self.Controller.start())
        prediction.daemon = True
        prediction.start()

    def save(self):
        pass

    def save_all(self):
        pass

    def cancel(self):
        pass

    def next_grayscale(self):
        print("next!!!!")
        print(len(self.grayscale_images))
        self.grayscale_index += 1
        print(self.grayscale_index)
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index], ext='jpg').texture

    def previous_grayscale(self):
        self.grayscale_index -= 1
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index], ext='jpg').texture

    def next_colorized(self):
        self.colorized_index += 1
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index], ext='jpg').texture

    def previous_colorized(self):
        self.colorized_index -= 1
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index], ext='jpg').texture


PhotosColorizationApp().run()
