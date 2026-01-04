# 从Kivy核心库导入两个必要类
# App：所有Kivy应用的基类，负责管理应用生命周期
# Label：基础文本显示控件，用于展示Hello World文本
from kivy.app import App
from kivy.uix.label import Label

# 定义自定义应用类，继承自kivy.app.App
class HelloWorldApp(App):
    # 重写build()方法：Kivy应用的界面构建入口，必须返回一个根控件
    def build(self):
        # 返回Label控件，核心是设置text属性为"Hello World"，配置字体大小便于查看
        return Label(text="Hello World", font_size=40)

# 程序入口，启动Kivy应用
if __name__ == '__main__':
    HelloWorldApp().run()
