from kivy.app import App
from kivy.core.window import Window


class PhotosColorizationApp(App):
    def build(self):
        Window.bind(on_dropfile=self.on_drop_file)
        return

    def tick_box(self, value):
        return

    def on_drop_file(self, window, file_path):
        print(file_path)
        return


PhotosColorizationApp().run()
