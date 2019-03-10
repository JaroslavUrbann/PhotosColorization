from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from threading import Thread
from kivy.clock import mainthread
from scripts.controller import Controller
from kivy.lang import Builder
import time
import sys
import os
from glob import glob
Window.size = (1024, 576)


class ErrorDialog(FloatLayout):
    ok = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveAllDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class PhotosColorizationApp(App):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    Controller = Controller()
    grayscale_images = []
    colorized_images = []
    grayscale_index = 0
    colorized_index = 0
    load_path = "/"
    save_path = "/"
    popup = None
    error_popup = None
    prediction_thread = None
    timer_period = 70
    old_id = ""

    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        Window.bind(mouse_pos=self.on_mouse_pos)
        load_models = Thread(target=self.Controller.load_models, args=(self.resource_path(""),))
        load_models.daemon = True
        load_models.start()
        self.root = Builder.load_file(self.resource_path('scripts/view.kv'))
        self.update_buttons()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def on_mouse_pos(self, *args):
        ids = self.root.ids
        x, y = args[1]
        id = \
            "load" if ids.load.pos[0] < x < ids.load.pos[0] + ids.load.size[0] and ids.load.pos[1] < y < ids.load.pos[1] + ids.load.size[1] else \
            "save" if ids.save.pos[0] < x < ids.save.pos[0] + ids.save.size[0] and ids.save.pos[1] < y < ids.save.pos[1] + ids.save.size[1] else \
            "start" if ids.start.pos[0] < x < ids.start.pos[0] + ids.start.size[0] and ids.start.pos[1] < y < ids.start.pos[1] + ids.start.size[1] else \
            "save_all" if ids.save_all.pos[0] < x < ids.save_all.pos[0] + ids.save_all.size[0] and ids.save_all.pos[1] < y < ids.save_all.pos[1] + ids.save_all.size[1] else \
            "cancel" if ids.cancel.pos[0] < x < ids.cancel.pos[0] + ids.cancel.size[0] and ids.cancel.pos[1] < y < ids.cancel.pos[1] + ids.cancel.size[1] else \
            "n_g" if ids.n_g.pos[0] < x < ids.n_g.pos[0] + ids.n_g.size[0] and ids.n_g.pos[1] < y < ids.n_g.pos[1] + ids.n_g.size[1] else \
            "p_g" if ids.p_g.pos[0] < x < ids.p_g.pos[0] + ids.p_g.size[0] and ids.p_g.pos[1] < y < ids.p_g.pos[1] + ids.p_g.size[1] else \
            "n_c" if ids.n_c.pos[0] < x < ids.n_c.pos[0] + ids.n_c.size[0] and ids.n_c.pos[1] < y < ids.n_c.pos[1] + ids.n_c.size[1] else \
            "p_c" if ids.p_c.pos[0] < x < ids.p_c.pos[0] + ids.p_c.size[0] and ids.p_c.pos[1] < y < ids.p_c.pos[1] + ids.p_c.size[1] else ""
        if self.old_id != id:
            if self.old_id != "":
                ids[self.old_id].background_color = (0.2, 0.2, 0.2, 1)
                self.old_id = ""
            if bool(id) and not ids[id].disabled:
                ids[id].background_color = (0.2902, 0.2902, 0.2902, 1)
                self.old_id = id

    def start_timer(self):
        start = 108
        length = 762
        start_time = time.time()
        while True:
            if self.root.ids.pb.value < start + length:
                self.root.ids.pb.value += 1

            if self.Controller.is_colorized() or not self.prediction_thread.is_alive():
                if self.Controller.is_colorized():
                    self.colorized_images.append(self.Controller.get_last_colorized())
                    self.colorized_index = len(self.colorized_images) - 1
                    self.colorized_images[self.colorized_index].seek(0)
                    self.update_colorized_gallery()
                    self.update_buttons()
                    self.timer_period = (time.time() - start_time) * 0.75 + self.timer_period * 0.25
                    print(self.timer_period)
                # finishes up the progressbar if it is still not finished and then resets it
                while self.root.ids.pb.value < start + length:
                    self.root.ids.pb.value += 1
                    time.sleep(0.5 / (.1 + length + start - self.root.ids.pb.value))
                self.root.ids.pb.value = start

                if not self.prediction_thread.is_alive() or len(self.colorized_images) >= len(self.grayscale_images):
                    print("breaks")
                    self.update_buttons()
                    return
                start_time = time.time()
            time.sleep(self.timer_period / length)

    @mainthread
    def update_colorized_gallery(self):
        self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index],
                                                                    ext='jpg').texture

    def on_drop_file(self, window, file_path):
        self.upload_images(str(file_path, 'UTF-8'))

    def load(self, file_paths, load_path):
        self.load_path = load_path
        # kivi sometimes counts in the folder you're in
        if len(file_paths) > 1:
            for path in file_paths[1:]:
                if file_paths[0] == os.path.dirname(path):
                    file_paths = file_paths[1:]
                    break
        for path in file_paths:
            self.upload_images(path)
            self.dismiss_popup()

    def upload_images(self, path):
        if not (self.prediction_thread.is_alive() if self.prediction_thread else False):
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
                    self.grayscale_images[self.grayscale_index].seek(0)
                    self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index],
                                                                ext='jpg').texture
            self.update_buttons()

    def dismiss_popup(self):
        self.popup.dismiss()

    def dismiss_error_popup(self):
        self.error_popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load image(s)", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def show_error(self):
        content = ErrorDialog(ok=self.dismiss_error_popup)
        self.error_popup = Popup(title="Error", content=content, size_hint=(0.3, 0.3))
        self.error_popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        content.ids.text_input.text = self.Controller.get_colorized_name(self.colorized_index)
        self.popup = Popup(title="Save image", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def show_save_all(self):
        content = SaveAllDialog(save=self.save_all, cancel=self.dismiss_popup)
        self.popup = Popup(title="Save images", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def update_buttons(self):
        self.root.ids.n_g.disabled = len(self.grayscale_images) <= self.grayscale_index + 1
        self.root.ids.p_g.disabled = self.grayscale_index < 1
        self.root.ids.n_c.disabled = len(self.colorized_images) <= self.colorized_index + 1
        self.root.ids.p_c.disabled = self.colorized_index < 1
        self.root.ids.start.disabled = not bool(self.grayscale_images) or (self.prediction_thread.is_alive() if self.prediction_thread else False)
        self.root.ids.load.disabled = self.prediction_thread.is_alive() if self.prediction_thread else False
        self.root.ids.save.disabled = len(self.colorized_images) == 0
        self.root.ids.save_all.disabled = len(self.colorized_images) == 0
        self.root.ids.grayscale_counter.text = (str(self.grayscale_index + 1) if self.grayscale_images else "0") + " / " + str(len(self.grayscale_images))
        self.root.ids.colorized_counter.text = (str(self.colorized_index + 1) if self.colorized_images else "0") + " / " + str(len(self.colorized_images))
        self.root.ids.done_counter.text = str(len(self.colorized_images)) + " / " + str(len(self.grayscale_images))
        self.root.ids.cancel.disabled = not (self.prediction_thread.is_alive() if self.prediction_thread else False)

    def start(self):
        self.colorized_images = []
        self.colorized_index = 0
        self.prediction_thread = Thread(target=self.Controller.start)
        self.prediction_thread.daemon = True
        self.prediction_thread.start()
        timer = Thread(target=self.start_timer)
        timer.daemon = True
        timer.start()
        self.update_buttons()
        print("I started them")

    def save(self, path, name):
        print(path)
        self.save_path = path
        if self.Controller.save(path, name, self.colorized_index):
            self.dismiss_popup()
        else:
            self.show_error()

    def save_all(self, path):
        if self.Controller.save_all(path):
            self.dismiss_popup()
        else:
            self.show_error()

    def cancel(self):
        self.Controller.cancel()
        self.update_buttons()
        self.root.ids.cancel.disabled = True

    def n_g(self):
        self.grayscale_index += 1
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index], ext='jpg').texture

    def p_g(self):
        self.grayscale_index -= 1
        self.update_buttons()
        self.grayscale_images[self.grayscale_index].seek(0)
        self.root.ids.grayscale_img.texture = CoreImage(self.grayscale_images[self.grayscale_index], ext='jpg').texture

    def n_c(self):
        self.colorized_index += 1
        self.update_buttons()
        self.colorized_images[self.colorized_index].seek(0)
        self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index], ext='jpg').texture

    def p_c(self):
        self.colorized_index -= 1
        self.update_buttons()
        self.colorized_images[self.colorized_index].seek(0)
        self.root.ids.colorized_img.texture = CoreImage(self.colorized_images[self.colorized_index], ext='jpg').texture


if __name__ == '__main__':
    PhotosColorizationApp().run()
