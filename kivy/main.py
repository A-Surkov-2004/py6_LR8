from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import face
from kivy.clock import Clock
from kivy.uix.switch import Switch

class DropImage(Image):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)
        self.app = app

    def _on_file_drop(self, window, file_path):
        self.app.path = file_path.decode("utf-8")
        self.source = file_path.decode("utf-8")  # Преобразуем путь в строку
        return True

class MainLayout(FloatLayout):
    img = ObjectProperty(None)  # Ссылка на изображение

class DragDropApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.switch = Switch(size_hint=(1, 0.1))
        self.delay = 0.1
        self.path = ""


    def update_frame(self, dt):
        if self.switch.active:
            face.loadFromImg(self.path)
        else:
            face.loadFromCam()

    def build(self):
        layout = MainLayout()
        layout.img = DropImage(self, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(layout.img)
        layout.add_widget(self.switch)

        Clock.schedule_interval(self.update_frame, self.delay)

        return layout

if __name__ == '__main__':
    DragDropApp().run()