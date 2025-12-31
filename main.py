# 导入Kivy核心组件（兼容Kivy 2.3.0，打包无报错）
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

# 配置窗口尺寸（适配手机屏幕，打包后自动适配不同设备）
Window.size = (480, 800)

# 定义App类，核心功能：显示“新年快乐2026”暖金色文本
class HappyNewYear2026App(App):
    def build(self):
        # 创建标签组件，设置文本样式
        label = Label(
            text="新年快乐 2026",  # 核心显示文本
            font_size=60,  # 字体大小，手机上清晰可见
            bold=True,  # 加粗显示，提升可读性
            color=(1, 0.8, 0, 1)  # 暖金色（红=1，绿=0.8，蓝=0，透明度=1）
        )
        return label

# 程序运行入口，兼容Python和Kivy打包规范
if __name__ == "__main__":
    HappyNewYear2026App().run()
