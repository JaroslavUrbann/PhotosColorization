from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
import controller
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
    popup = None
    grayscale_img = ("img", 0, 0)
    colorized_img = ("img", 0, 0)
    is_loaded = False
    is_working = False

    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        self.update_buttons()
        return

    def on_drop_file(self, window, file_path):
        if not self.is_working:
            self.is_loaded = self.Controller.set_image_paths(str(file_path, 'UTF-8'))
            self.update_buttons()
        return

    def update_buttons(self):
        self.root.next_grayscale.disabled = self.grayscale_img[1] == self.grayscale_img[2]
        self.root.previous_grayscale.disabled = self.grayscale_img[1] <= 1
        self.root.next_colorized.disabled = self.colorized_img[1] == self.colorized_img[2]
        self.root.previous_colorized.disabled = self.colorized_img[1] <= 1
        self.root.start.disabled = not self.is_loaded and self.is_working
        self.root.load.disabled = self.is_working
        self.root.save.disabled = self.colorized_img[1] == 0
        self.root.save_all.disabled = self.colorized_img[1] == 0

    def start(self):
        pass

    def save(self):
        pass

    def save_all(self):
        pass

    def cancel(self):
        pass

    def next_grayscale(self):
        self.grayscale_img = self.Controller.next_grayscale(self.grayscale_img)
        self.update_buttons()
        # self.root.grayscale_img.texture = CoreImage(self.grayscale_img[0], ext='jpg').texture

    def previous_grayscale(self):
        self.grayscale_img = self.Controller.previous_grayscale(self.grayscale_img)
        self.update_buttons()
        # self.root.grayscale_img.texture = CoreImage(self.grayscale_img[0], ext='jpg').texture

    def next_colorized(self):
        self.colorized_img = self.Controller.next_colorized(self.colorized_img)
        self.update_buttons()
        # self.root.colorized_img.texture = CoreImage(self.colorized_img[0], ext='jpg').texture

    def previous_colorized(self):
        self.colorized_img = self.Controller.previous_colorized(self.colorized_img)
        self.update_buttons()
        # self.root.colorized_img.texture = CoreImage(self.colorized_img[0], ext='jpg').texture

    def dismiss_popup(self):
        self.popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self.popup.open()
        self.root.ids.grayscale_img.source = "assets/d.jpg"

    def load(self, path, file_path):
        self.is_loaded = self.Controller.set_image_paths(file_path[0])
        self.update_buttons()
        self.dismiss_popup()


PhotosColorizationApp().run()
