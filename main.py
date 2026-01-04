from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random
import math


# 粒子类：管理烟花爆炸后的单个粒子（保留核心逻辑，优化粒子数量让满屏更饱满）
class Particle:
    def __init__(self, x, y):
        # 粒子初始位置（烟花爆炸中心）
        self.x = x
        self.y = y

        # 随机生成粒子爆炸方向（0-360度）
        angle = random.uniform(0, 2 * math.pi)
        # 随机生成粒子爆炸速度（微调范围，让满屏烟花更均匀）
        speed = random.uniform(1.5, 4.5)

        # 分解为x、y方向的速度
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # 随机生成烟花颜色（暖色调为主，保留透明度衰减）
        self.r = random.uniform(0.8, 1.0)  # 红
        self.g = random.uniform(0.2, 0.9)  # 绿
        self.b = random.uniform(0.0, 0.8)  # 蓝
        self.a = 1.0  # 透明度（逐渐衰减）

        # 粒子生命周期（帧数，微调让效果更持久）
        self.life = random.randint(25, 55)
        # 粒子大小
        self.size = random.uniform(1.8, 3.8)

        # 重力系数（模拟粒子下落）
        self.gravity = 0.02

    def update(self):
        """更新粒子的位置、速度、生命周期和透明度"""
        # 应用重力（y方向速度衰减，模拟下落）
        self.vy -= self.gravity

        # 更新粒子位置
        self.x += self.vx
        self.y += self.vy

        # 生命周期倒计时
        self.life -= 1

        # 透明度随生命周期衰减（逐渐消失）
        self.a = max(0, self.life / 60)


# 烟花类：管理单个烟花的爆炸和粒子集合（修改爆炸位置实现满屏效果）
class Firework:
    def __init__(self):
        # 优化：爆炸位置覆盖整个屏幕（0到窗口宽/高，不再限制中间区域）
        self.x = random.uniform(0, Window.width)  # 横向满屏
        self.y = random.uniform(0, Window.height)  # 纵向满屏

        # 微调粒子数量（让满屏烟花更饱满，不杂乱）
        self.particles = [Particle(self.x, self.y) for _ in range(random.randint(45, 95))]

    def update(self):
        """更新所有粒子的状态，返回是否还有存活粒子"""
        for particle in self.particles:
            particle.update()

        # 过滤掉生命周期结束的粒子
        self.particles = [p for p in self.particles if p.life > 0]

        # 返回是否还有存活粒子（无存活则烟花消失）
        return len(self.particles) > 0


# 烟花画布：负责绘制和管理所有烟花（保留核心绘制逻辑）
class FireworkCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 烟花集合
        self.fireworks = []

        # 定时刷新动画（60帧/秒）
        Clock.schedule_interval(self.update, 1 / 60)

        # 定时生成新烟花（微调间隔，让满屏烟花更连贯）
        self.schedule_new_firework()

    def schedule_new_firework(self):
        """定时生成新烟花，递归调用实现持续生成"""
        self.add_firework()
        # 随机间隔（400-900毫秒）生成下一个烟花，提升满屏连贯性
        Clock.schedule_once(lambda dt: self.schedule_new_firework(), random.uniform(0.4, 0.9))

    def add_firework(self):
        """添加一个新烟花"""
        self.fireworks.append(Firework())

    def update(self, dt):
        """更新所有烟花状态并重新绘制"""
        # 清空画布
        self.canvas.clear()

        # 迭代更新所有烟花，过滤掉已消失的烟花
        active_fireworks = []
        for firework in self.fireworks:
            if firework.update():
                active_fireworks.append(firework)
                # 绘制当前烟花的所有粒子
                self.draw_firework(firework)
        self.fireworks = active_fireworks

    def draw_firework(self, firework):
        """绘制单个烟花的所有粒子"""
        for particle in firework.particles:
            with self.canvas:
                # 设置粒子颜色（包含透明度衰减）
                Color(particle.r, particle.g, particle.b, particle.a)
                # 绘制粒子（椭圆，模拟圆形光点）
                Ellipse(
                    pos=(particle.x - particle.size / 2, particle.y - particle.size / 2),
                    size=(particle.size, particle.size)
                )


# 主布局：叠加烟花画布和垂直文字（实现文字与烟花共存）
class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 1. 添加烟花画布（占满整个屏幕）
        self.firework_canvas = FireworkCanvas()
        self.add_widget(self.firework_canvas)

        # 2. 创建垂直布局（实现文字从上到下排版）
        self.text_layout = BoxLayout(
            orientation='vertical',  # 垂直排列（从上到下）
            spacing=15,  # 字与字之间的间距
            size_hint=(None, None),  # 固定布局大小，不随窗口拉伸
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # 居中显示（可调整位置）
        )

        # 3. 定义要显示的文字（拆分单个字符，实现从上到下每个字一行）
        welcome_text = "欢迎姜文斌"

        # 4. 为每个字符创建Label，添加到垂直布局中
        for char in welcome_text:
            label = Label(
                text=char,
                font_size=48,  # 字体大小（可调整）
                bold=True,  # 加粗显示
                color=get_color_from_hex("#FFFFFF"),  # 白色文字，与烟花形成对比
                shadow_color=(0, 0, 0, 0.8),  # 文字阴影，提升可读性
                shadow_offset=(2, -2)  # 阴影偏移量
            )
            self.text_layout.add_widget(label)

        # 5. 将文字布局添加到主布局中
        self.add_widget(self.text_layout)


# 烟花应用主类（优化布局，保留窗口设置）
class FireworkApp(App):
    def build(self):
        # 设置窗口大小
        Window.size = (800, 600)
        # 设置窗口标题
        self.title = "欢迎姜文斌 - 满屏烟花效果"
        # 返回主布局（包含烟花和文字）
        return MainLayout()


if __name__ == "__main__":
    FireworkApp().run()
