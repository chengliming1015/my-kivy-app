from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyKivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        title_label = Label(
            text="Kivy GitHub Actions 打包示例",
            font_size=30,
            bold=True
        )
        desc_label = Label(
            text="APK 构建成功！\n可直接复用此模板开发上层功能",
            font_size=20
        )
        layout.add_widget(title_label)
        layout.add_widget(desc_label)
        return layout

if __name__ == '__main__':
    MyKivyApp().run()
