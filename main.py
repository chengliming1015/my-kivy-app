# 导入 Kivy 核心必要模块
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# 定义应用主类，继承自 Kivy 的 App 类
class HelloJiangContentApp(App):
    # 核心方法：构建应用界面
    def build(self):
        # 1. 创建根布局容器（BoxLayout），承载蓝底和内容
        root_layout = BoxLayout(
            # 蓝底背景（RGBA 格式，舒适明亮蓝，不透明）
            background_color=(0, 0.4, 0.8, 1),
            # 内边距：让内容与窗口边缘保持合理距离，符合内容阅读习惯
            padding=(40, 40, 40, 40)
        )
        
        # 2. 创建内容标签（Label），展示「你好，姜文斌」，引用 fonts 目录下的字体
        content_label = Label(
            # 内容文本
            text="你好，姜文斌",
            # 文字颜色：深灰色，柔和不刺眼，贴合内容属性
            color=(0.1, 0.1, 0.1, 1),
            # 字体大小：24号，符合内容展示的视觉舒适度
            font_size=24,
            # 文字水平对齐：左对齐，贴近阅读逻辑
            halign="left",
            # 文字垂直对齐：顶部对齐
            valign="top",
            # 关键：设置文本宽度适配布局，支持后续多行内容自动换行
            text_size=(None, None),
            # 自适应布局：宽度占满、高度自适应文本
            size_hint=(1, None),
            height=self.texture_size[1],
            # 核心修改：指定字体的相对路径（fonts 目录下的 msyhbd.ttc）
            font_name="fonts/msyhbd.ttc"
        )
        
        # 3. 将内容标签添加到根布局中
        root_layout.add_widget(content_label)
        
        # 4. 返回根布局，作为应用显示界面
        return root_layout

# 程序入口：运行 Kivy 应用
if __name__ == "__main__":
    HelloJiangContentApp().run()
