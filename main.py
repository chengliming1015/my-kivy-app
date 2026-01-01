from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
import random
from math import sin, cos, pi

# 配置背景（深黑星空，突出烟花）+ 禁用屏保（避免播放中断）
Window.clearcolor = get_color_from_hex('#000015')
Window.allow_screensaver = False

class FireworkParticle:
    """烟花粒子类，控制单个粒子的运动、生命周期和视觉效果"""
    def __init__(self, x, y):
        self.x = x  # 粒子初始x坐标
        self.y = y  # 粒子初始y坐标
        self.angle = random.uniform(0, 2 * pi)  # 随机运动角度
        self.speed = random.uniform(2, 5)  # 随机运动速度
        self.vx = cos(self.angle) * self.speed  # x方向速度分量
        self.vy = sin(self.angle) * self.speed  # y方向速度分量
        self.size = random.uniform(2, 4)  # 粒子初始大小
        # 随机鲜艳烟花颜色（红/橙/黄/绿/蓝/紫）
        self.color = random.choice([(1,0,0),(1,0.5,0),(1,1,0),(0,1,0),(0,0,1),(0.6,0,1)])
        self.life = 60  # 粒子生命周期（帧数）
        self.alpha = 1.0  # 粒子透明度（渐变消失）

    def update(self):
        """更新粒子状态，实现重力、减速、透明渐变效果"""
        # 更新粒子位置
        self.x += self.vx
        self.y += self.vy
        # 模拟轻微重力，粒子缓慢下落
        self.vy -= 0.02
        # 速度衰减，粒子逐渐减速
        self.vx *= 0.98
        self.vy *= 0.98
        # 生命周期减少，透明度同步降低
        self.life -= 1
        self.alpha = self.life / 60
        # 粒子轻微缩小，增强真实感
        self.size *= 0.99

class FireworkWidget(Widget):
    """主界面控件，管理烟花生成、更新和2026欢迎文字展示"""
    def __init__(self, **kwargs):
        super().__init__(** kwargs)
        self.particles = []  # 存储所有活跃烟花粒子
        self.add_welcome_label()  # 添加居中欢迎文字
        # 定时任务：60帧/秒更新界面 + 每1.2秒生成一朵烟花
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_firework, 1.2)

    def add_welcome_label(self):
        """添加居中对齐的2026欢迎文字"""
        welcome_label = Label(
            text="Welcome to 2026\n新年快乐 万事顺意",
            font_size=42,
            color=(1, 1, 1, 0.95),  # 白色高透明度，清晰不刺眼
            halign='center',
            valign='middle',
            size_hint=(1, 1)  # 铺满窗口，实现自动居中
        )
        self.add_widget(welcome_label)

    def spawn_firework(self, dt):
        """生成一朵新烟花（随机窗口位置，90-130个粒子）"""
        x = random.uniform(Window.width * 0.2, Window.width * 0.8)
        y = random.uniform(Window.height * 0.3, Window.height * 0.7)
        for _ in range(random.randint(90, 130)):
            self.particles.append(FireworkParticle(x, y))

    def update(self, dt):
        """更新所有粒子状态，清理过期粒子，绘制当前帧"""
        # 清理生命周期结束的粒子（避免内存泄漏）
        self.particles = [p for p in self.particles if p.life > 0]
        # 绘制所有活跃粒子
        with self.canvas:
            for particle in self.particles:
                Color(*particle.color, particle.alpha)
                Ellipse(
                    pos=(particle.x - particle.size/2, particle.y - particle.size/2),
                    size=(particle.size, particle.size)
                )
                # 更新粒子当前状态
                particle.update()

class Firework2026App(App):
    """Kivy主应用类，启动烟花欢迎页面"""
    def build(self):
        self.title = "2026烟花欢迎页"
        return FireworkWidget()

if __name__ == '__main__':
    Firework2026App().run()
