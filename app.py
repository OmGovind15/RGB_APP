from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class RGBDetector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.image = Image()
        self.add_widget(self.image)

        self.label = Label(text="Select an image to detect RGB values", size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.file_chooser = FileChooserIconView(size_hint=(1, 0.5))
        self.file_chooser.bind(on_selection=self.load_image)
        self.add_widget(self.file_chooser)

        self.capture_button = Button(text="Capture from Camera", size_hint=(1, 0.1))
        self.capture_button.bind(on_press=self.capture_image)
        self.add_widget(self.capture_button)

    def load_image(self, instance, selection):
        if selection:
            image_path = selection[0]
            self.process_image(image_path)

    def capture_image(self, instance):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()

        if ret:
            image_path = "captured_image.png"
            cv2.imwrite(image_path, frame)
            self.process_image(image_path)

    def process_image(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        avg_color = np.mean(img, axis=(0, 1))  # Calculate average RGB
        r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
        self.label.text = f"Average RGB: ({r}, {g}, {b})"

        img = cv2.flip(img, 0)
        buf = img.tobytes()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt="rgb")
        texture.blit_buffer(buf, colorfmt="rgb", bufferfmt="ubyte")
        self.image.texture = texture

class RGBApp(App):
    def build(self):
        return RGBDetector()

if __name__ == "__main__":
    RGBApp().run()


