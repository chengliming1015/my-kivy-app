from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, Rotate, Translate
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import random
from math import hypot

# ✅ 手机竖屏适配（核心）
Window.size = (360, 640)
Window.clearcolor = get_color_from_hex('#000020')  # 深蓝夜景底
Window.fullscreen = False  # 打包后可改True全屏

# 圣诞配色常量
COLOR_GREEN = get_color_from_hex('#008822')
COLOR_LIGHT_GREEN = get_color_from_hex('#00cc33')
COLOR_RED = get_color_from_hex('#ff2222')
COLOR_GOLD = get_color_from_hex('#ffdd00')
COLOR_WHITE = get_color_from_hex('#ffffff')
COLOR_BROWN = get_color_from_hex('#885522')

class ChristmasTreeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 核心变量
        self.particles = []  # 装饰粒子
        self.snows = []      # 雪花粒子
        self.scale_val = 1.0 # 缩放比例
        self.last_touches = [] # 双指触控记录
        self.tree_center = (self.center_x, self.y + dp(180)) # 圣诞树中心
        self.music = None    # 圣诞音乐
        self.flash_flag = False # 点击闪烁标记

        # 初始化资源
        self.init_tree()     # 绘制圣诞树主体
        self.init_music()    # 加载圣诞音乐
        Clock.schedule_interval(self.update, 1/60) # 60帧动画刷新
        Clock.schedule_interval(self.add_snow, 1/10)# 雪花生成频率

    # ✅ 初始化圣诞树主体（三层枝叶+树干+星星顶）
    def init_tree(self):
        cx, cy = self.tree_center
        with self.canvas.before:
            # 树干
            Color(*COLOR_BROWN)
            Rectangle(pos=(cx-dp(15), cy-dp(120)), size=(dp(30), dp(80)))
            # 三层圣诞树枝叶（渐变绿）
            Color(*COLOR_GREEN)
            Ellipse(pos=(cx-dp(70), cy-dp(20)), size=(dp(140), dp(100)))
            Color(*COLOR_LIGHT_GREEN)
            Ellipse(pos=(cx-dp(50), cy+dp(50)), size=(dp(100), dp(80)))
            Color(*COLOR_GREEN)
            Ellipse(pos=(cx-dp(30), cy+dp(100)), size=(dp(60), dp(60)))
            # 顶部星星（金色）
            Color(*COLOR_GOLD)
            Line(points=[cx, cy+dp(140), cx-dp(10), cy+dp(120), cx+dp(10), cy+dp(120), cx, cy+dp(140)], width=dp(2))

    # ✅ 加载圣诞音乐（打包时需把music.mp3放同目录）
    def init_music(self):
        try:
            self.music = SoundLoader.load('music.mp3')
            if self.music:
                self.music.loop = True  # 循环播放
        except:
            pass # 无音乐文件不报错

    # ✅ 生成雪花粒子
    def add_snow(self, dt):
        x = random.randint(0, int(self.width))
        y = self.height + dp(10)
        size = random.randint(1, 4)
        speed = random.uniform(1, 3)
        self.snows.append({'x':x, 'y':y, 'size':size, 'speed':speed})

    # ✅ 生成圣诞装饰粒子（红/金/白）
    def add_particle(self):
        cx, cy = self.tree_center
        x = random.randint(int(cx-dp(60)), int(cx+dp(60)))
        y = random.randint(int(cy-dp(20)), int(cy+dp(120)))
        size = random.randint(3, 6)
        color = random.choice([COLOR_RED, COLOR_GOLD, COLOR_WHITE])
        self.particles.append({'x':x, 'y':y, 'size':size, 'color':color, 'flash':False})

    # ✅ 点击屏幕：闪烁特效+播放音乐
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # 播放音乐
            if self.music and not self.music.state == 'play':
                self.music.play()
            # 点击闪烁
            self.flash_flag = True
            # 生成装饰粒子
            for _ in range(5):
                self.add_particle()
        return super().on_touch_down(touch)

    # ✅ 双指捏合缩放圣诞树（核心手势）
    def on_touch_move(self, touch):
        if len(self.touches) == 2:
            t1, t2 = self.touches[:2]
            # 计算双指距离
            dist_now = hypot(t1.x-t2.x, t1.y-t2.y)
            if self.last_touches:
                dist_prev = hypot(self.last_touches[0].x-self.last_touches[1].x,
                                  self.last_touches[0].y-self.last_touches[1].y)
                # 更新缩放比例
                self.scale_val += (dist_now - dist_prev) * 0.001
                self.scale_val = max(0.5, min(self.scale_val, 2.0)) # 缩放限制0.5-2倍
            self.last_touches = [t1, t2]
        return super().on_touch_move(touch)

    # ✅ 动画主更新（粒子+雪花+缩放+闪烁）
    def update(self, dt):
        self.canvas.after.clear()
        cx, cy = self.tree_center

        # 应用缩放变换
        with self.canvas.after:
            Translate(cx, cy)
            Rotate(0)
            Translate(-cx, -cy)
            Scale(self.scale_val, self.scale_val, 1, origin=(cx, cy))

            # 绘制装饰粒子
            for p in self.particles:
                Color(*p['color'], 1 if not p['flash'] else 0.3)
                Ellipse(pos=(p['x']-p['size']/2, p['y']-p['size']/2), size=(p['size'], p['size']))
                p['flash'] = not p['flash'] # 闪烁效果
                if random.random() < 0.01:
                    p['size'] += 0.1 # 随机缩放

            # 绘制雪花粒子
            for s in self.snows:
                Color(*COLOR_WHITE, 0.8)
                Ellipse(pos=(s['x']-s['size']/2, s['y']-s['size']/2), size=(s['size'], s['size']))
                s['y'] -= s['speed'] # 雪花下落
                s['x'] += random.uniform(-0.5, 0.5) # 雪花左右飘

            # 点击全局闪烁
            if self.flash_flag:
                Color(*COLOR_WHITE, 0.5)
                Ellipse(pos=(cx-dp(100), cy-dp(100)), size=(dp(200), dp(200)))
                self.flash_flag = False

        # 清理出界粒子
        self.particles = [p for p in self.particles if 0 < p['x'] < self.width and 0 < p['y'] < self.height]
        self.snows = [s for s in self.snows if s['y'] > -dp(10)]

        # 持续生成装饰粒子
        if random.random() < 0.05:
            self.add_particle()

# ✅ 主APP类
class ChristmasTreeApp(App):
    title = "Gemini3圣诞树-Kivy版"
    def build(self):
        return ChristmasTreeWidget()

if __name__ == '__main__':
    ChristmasTreeApp().run()
