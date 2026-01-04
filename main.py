from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from random import random, randint, uniform

# 配置窗口大小（可选，可自行调整）
Window.size = (800, 600)
# 窗口标题
Window.title = "欢迎姜文斌 - 蓝色背景烟花秀"

class FireworkParticle:
    """烟花粒子类，负责单个粒子的属性和更新"""
    def __init__(self, x, y):
        # 粒子初始位置
        self.x = x
        self.y = y
        # 粒子初始速度（随机方向，有向上的初速度）
        self.vx = uniform(-3, 3)
        self.vy = uniform(2, 5)
        # 粒子大小（随机）
        self.size = uniform(1, 3)
        # 粒子颜色（随机暖色调，模拟烟花）
        self.r = random()
        self.g = random() * 0.7  # 降低绿色值，更贴近真实烟花
        self.b = random() * 0.5  # 降低蓝色值，避免和背景冲突
        # 粒子生命周期（逐渐消失）
        self.life = 100
        self.alpha = 1.0

    def update(self):
        """更新粒子的位置、生命周期和透明度"""
        # 加入重力效果，让粒子逐渐下落
        self.vy -= 0.05
        # 更新位置
        self.x += self.vx
        self.y += self.vy
        # 更新生命周期和透明度
        self.life -= 1
        self.alpha = self.life / 100
        # 确保透明度不小于0
        if self.alpha < 0:
            self.alpha = 0

class FireworkWidget(Widget):
    """主控件，负责绘制背景、文字和烟花"""
    def __init__(self, **kwargs):
        super(FireworkWidget, self).__init__(**kwargs)
        # 初始化烟花粒子列表
        self.firework_particles = []
        # 绘制蓝色背景
        self._draw_background()
        # 调度定时器：持续生成烟花（每0.3秒生成一组）
        Clock.schedule_interval(self._spawn_firework, 0.3)
        # 调度定时器：持续更新和绘制烟花（每帧更新）
        Clock.schedule_interval(self._update_fireworks, 1/60)

    def _draw_background(self):
        """绘制蓝色背景"""
        with self.canvas.before:
            # 蓝色背景（可调整RGB值修改深浅，当前为天蓝色）
            Color(0.1, 0.3, 0.6, 1.0)
            self.background = Rectangle(pos=self.pos, size=self.size)
            # 绑定背景大小到窗口大小，窗口缩放时背景同步更新
            self.bind(pos=self._update_background, size=self._update_background)

    def _update_background(self, *args):
        """更新背景大小（窗口缩放时触发）"""
        self.background.pos = self.pos
        self.background.size = self.size

    def _spawn_firework(self, *args):
        """生成一组新的烟花粒子（随机位置）"""
        # 随机选择烟花生成位置（窗口内）
        spawn_x = randint(100, Window.width - 100)
        spawn_y = randint(100, Window.height - 300)
        # 生成一组粒子（每组50-80个，保证烟花效果饱满）
        for _ in range(randint(50, 80)):
            particle = FireworkParticle(spawn_x, spawn_y)
            self.firework_particles.append(particle)

    def _update_fireworks(self, *args):
        """更新烟花粒子状态并重新绘制"""
        # 清空之前的烟花绘制
        self.canvas.after.clear()

        # 绘制“欢迎姜文斌”文字（居中显示，白色）
        with self.canvas.after:
            Color(1.0, 1.0, 1.0, 1.0)  # 白色
            # 文字绘制（Kivy默认字体，若需优化中文字体可额外配置）
            self._draw_text()

        # 更新并绘制所有烟花粒子
        alive_particles = []
        for particle in self.firework_particles:
            particle.update()
            # 只保留存活的粒子（生命周期>0）
            if particle.life > 0:
                alive_particles.append(particle)
                # 绘制单个粒子
                with self.canvas.after:
                    Color(particle.r, particle.g, particle.b, particle.alpha)
                    Ellipse(
                        pos=(particle.x, particle.y),
                        size=(particle.size, particle.size)
                    )
        # 更新粒子列表，移除死亡粒子（节省内存）
        self.firework_particles = alive_particles

    def _draw_text(self):
        """绘制居中文字“欢迎姜文斌”"""
        # 简化文字绘制（若需更美观的文字样式，可使用Label控件，效果一致）
        from kivy.graphics import PushMatrix, PopMatrix, Translate
        from kivy.core.text import Label as CoreLabel

        # 配置核心文字标签
        core_label = CoreLabel(
            text="欢迎姜文斌",
            font_size=48,
            color=(1, 1, 1, 1)
        )
        core_label.refresh()

        # 文字居中计算
        text_x = (Window.width - core_label.texture_size[0]) / 2
        text_y = (Window.height - core_label.texture_size[1]) / 2

        # 绘制文字到画布
        with self.canvas.after:
            PushMatrix()
            Translate(text_x, text_y)
            Rectangle(texture=core_label.texture, size=core_label.texture_size)
            PopMatrix()

class FireworkApp(App):
    """Kivy应用主类"""
    def build(self):
        return FireworkWidget()

if __name__ == "__main__":
    FireworkApp().run()
