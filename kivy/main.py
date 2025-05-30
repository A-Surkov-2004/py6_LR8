from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import face
from kivy.clock import Clock
from kivy.uix.switch import Switch
from kivy.graphics.texture import Texture


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
        self.layout = MainLayout()

    def update_frame(self, dt):
        if self.switch.active:
            img_rgb = face.loadFromImg(self.path)

        else:
            img_rgb = face.loadFromCam()

        if type(img_rgb) is not type(None):
            # Создаем текстуру Kivy
            texture = Texture.create(size=(img_rgb.shape[1], img_rgb.shape[0]), colorfmt='rgb')
            texture.blit_buffer(img_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            texture.uvpos = (0, 1)
            texture.uvsize = (1, -1)

            # Применяем текстуру к Image
            self.layout.img.texture = texture


    def build(self):

        self.layout.img = DropImage(self, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.layout.img)
        self.layout.add_widget(self.switch)

        Clock.schedule_interval(self.update_frame, self.delay)

        return self.layout


if __name__ == '__main__':
    DragDropApp().run()
