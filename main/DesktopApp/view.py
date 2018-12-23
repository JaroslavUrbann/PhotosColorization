from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import controller
import time
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

    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        return

    def on_drop_file(self, window, file_path):
        print(file_path)
        print(self.Controller.set_image_paths(str(file_path, 'UTF-8')))
        print(self.Controller.image_paths)
        return

    def dismiss_popup(self):
        self.popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def load(self, path, file_path):
        print(self.Controller.set_image_paths(file_path[0]))
        print(self.Controller.image_paths)

        self.dismiss_popup()


PhotosColorizationApp().run()
