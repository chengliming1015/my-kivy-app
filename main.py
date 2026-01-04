from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class SimpleBlueBgApp(App):
    def build(self):
        # 1. 创建标签控件，设置文字和样式
        label = Label(
            text="欢迎姜文斌",
            font_size=48,  # 文字大小
            color=(1, 1, 1, 1)  # 文字颜色：白色
        )
        
        # 2. 绘制蓝色背景（绑定到标签控件，自适应窗口）
        with label.canvas.before:
            Color(0.1, 0.3, 0.6, 1.0)  # 天蓝色背景
            self.background = Rectangle(pos=label.pos, size=label.size)
        
        # 3. 绑定背景大小，窗口缩放时背景同步更新
        label.bind(pos=self.update_background, size=self.update_background)
        
        return label
    
    def update_background(self, instance, value):
        """更新背景大小，适配窗口缩放"""
        self.background.pos = instance.pos
        self.background.size = instance.size

if __name__ == "__main__":
    SimpleBlueBgApp().run()
