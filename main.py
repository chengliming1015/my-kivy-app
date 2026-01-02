from kivy.app import App
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        return Label(text='Hello Kivy! 官方零错打包', font_size=50)

if __name__ == '__main__':
    MainApp().run()
