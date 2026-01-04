"""
烟花绽放效果 - 欢迎姜文斌
屏幕中央显示"欢迎姜文斌"的烟花特效应用
"""

import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import (
    NumericProperty, ListProperty, 
    BooleanProperty, StringProperty
)
import colorsys
import os
from pathlib import Path
from datetime import datetime

# 设置窗口大小和背景色
Window.clearcolor = (0.05, 0.05, 0.1, 1)  # 深蓝色夜空背景
Window.size = (1200, 800)  # 更大的窗口
Window.title = "烟花绽放特效"  # 窗口标题，不是内容

# 注册字体
try:
    font_dir = Path(__file__).parent / 'fonts'
    font_path = font_dir / 'msyhbd.ttc'
    
    if font_path.exists():
        LabelBase.register(
            name='MicrosoftYaHei',
            fn_regular=str(font_path)
        )
        CHINESE_FONT = 'MicrosoftYaHei'
    else:
        # 如果没有找到字体，尝试系统字体
        import platform
        system = platform.system()
        if system == 'Windows':
            windows_font = 'C:/Windows/Fonts/msyh.ttc'
            if os.path.exists(windows_font):
                LabelBase.register(name='MicrosoftYaHei', fn_regular=windows_font)
                CHINESE_FONT = 'MicrosoftYaHei'
            else:
                CHINESE_FONT = 'Arial'
        else:
            CHINESE_FONT = 'Arial'
except Exception as e:
    print(f"字体设置警告: {e}")
    CHINESE_FONT = 'Arial'


class FireworkParticle(Widget):
    """烟花粒子"""
    size = NumericProperty(8)
    color = ListProperty([1, 1, 1, 1])
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    gravity = NumericProperty(0.1)
    decay = NumericProperty(0.97)
    life = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = random.uniform(4, 12)
        self.life = random.uniform(0.8, 1.5)
        
    def update(self, dt):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y -= self.gravity
        self.velocity_x *= self.decay
        self.velocity_y *= self.decay
        self.life -= dt * 0.5
        self.color[3] = self.life
        self.size = max(2, self.size * 0.99)
        return self.life > 0.1


class Firework(Widget):
    """单个烟花"""
    particles = ListProperty([])
    exploded = BooleanProperty(False)
    trail = ListProperty([])
    trail_length = NumericProperty(15)
    color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, x, y, color=None, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        
        if color:
            self.color = color
        else:
            hue = random.random()
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
            self.color = [rgb[0], rgb[1], rgb[2], 1]
        
        self.velocity_y = random.uniform(8, 12)
        self.velocity_x = random.uniform(-1, 1)
        self.trail = [(x, y)]
        
        # 核心粒子
        core = FireworkParticle()
        core.pos = self.pos
        core.color = self.color
        core.size = 12
        self.particles.append(core)
    
    def update(self, dt):
        if not self.exploded:
            self.y += self.velocity_y
            self.x += self.velocity_x
            self.velocity_y -= 0.1
            
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)
            
            if self.velocity_y < 0.5 or random.random() < 0.02:
                self.explode()
        else:
            alive_particles = []
            for particle in self.particles:
                if particle.update(dt):
                    alive_particles.append(particle)
            self.particles = alive_particles
        
        return len(self.particles) > 0 or not self.exploded
    
    def explode(self):
        if self.exploded:
            return
            
        self.exploded = True
        num_particles = random.randint(80, 150)
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            
            particle = FireworkParticle()
            particle.pos = self.pos
            
            # 颜色变化
            hue_shift = random.uniform(-0.1, 0.1)
            hsv = colorsys.rgb_to_hsv(self.color[0], self.color[1], self.color[2])
            new_hue = (hsv[0] + hue_shift) % 1.0
            rgb = colorsys.hsv_to_rgb(new_hue, hsv[1], hsv[2])
            particle.color = [rgb[0], rgb[1], rgb[2], 1]
            
            particle.velocity_x = math.cos(angle) * speed
            particle.velocity_y = math.sin(angle) * speed
            particle.size = random.uniform(4, 10)
            particle.gravity = random.uniform(0.05, 0.15)
            
            self.particles.append(particle)
        
        self.particles = self.particles[1:]


class WelcomeMessage(Widget):
    """欢迎消息组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 设置位置和大小
        self.size = (1000, 300)
        self.pos = (Window.width/2 - 500, Window.height/2 - 100)
        
        # 主标题：欢迎姜文斌
        self.main_label = Label(
            text="欢迎姜文斌",
            font_name=CHINESE_FONT,
            font_size=96,
            bold=True,
            color=(1, 1, 1, 1),
            size=self.size,
            pos=self.pos,
            halign='center',
            valign='middle'
        )
        self.main_label.text_size = self.size
        
        # 添加发光效果
        with self.main_label.canvas.before:
            Color(0, 0.5, 1, 0.3)  # 蓝色光晕
            Rectangle(pos=(self.pos[0]-10, self.pos[1]-10), 
                     size=(self.size[0]+20, self.size[1]+20))
            Color(1, 0.8, 0, 0.2)  # 金色光晕
            Rectangle(pos=(self.pos[0]-5, self.pos[1]-5), 
                     size=(self.size[0]+10, self.size[1]+10))
        
        self.add_widget(self.main_label)
        
        # 添加动画
        self.start_animations()
    
    def start_animations(self):
        """启动文字动画"""
        # 颜色渐变动画
        color_anim = Animation(color=(1, 0.8, 0, 1), duration=2) + \
                     Animation(color=(1, 0.5, 0.8, 1), duration=2) + \
                     Animation(color=(0.5, 1, 0.8, 1), duration=2) + \
                     Animation(color=(1, 1, 1, 1), duration=2)
        color_anim.repeat = True
        color_anim.start(self.main_label)
        
        # 脉动动画
        pulse_anim = Animation(font_size=100, duration=1.5) + \
                     Animation(font_size=96, duration=1.5)
        pulse_anim.repeat = True
        pulse_anim.start(self.main_label)
        
        # 轻微浮动动画
        float_anim = Animation(y=self.y+5, duration=2) + \
                     Animation(y=self.y-5, duration=2)
        float_anim.repeat = True
        float_anim.start(self)


class FireworksDisplay(FloatLayout):
    """烟花显示主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 存储烟花
        self.fireworks = []
        
        # 添加欢迎消息（屏幕中央）
        self.welcome_message = WelcomeMessage()
        self.add_widget(self.welcome_message)
        
        # 添加副标题
        self.subtitle = Label(
            text="🎆 烟花为您绽放 🎆",
            font_name=CHINESE_FONT,
            font_size=36,
            color=(0.9, 0.9, 1, 0.9),
            size=(800, 100),
            pos=(Window.width/2 - 400, Window.height/2 - 200),
            halign='center'
        )
        self.subtitle.text_size = (800, 100)
        self.add_widget(self.subtitle)
        
        # 添加底部信息
        self.info_label = Label(
            text="点击屏幕添加更多烟花 | 按ESC键退出",
            font_size=20,
            color=(0.7, 0.7, 0.7, 0.7),
            size=(600, 50),
            pos=(Window.width/2 - 300, 20),
            halign='center'
        )
        self.info_label.text_size = (600, 50)
        self.add_widget(self.info_label)
        
        # 添加时间显示
        self.time_label = Label(
            text=self.get_current_time(),
            font_size=18,
            color=(0.8, 0.8, 0.8, 0.6),
            pos=(20, Window.height - 40)
        )
        self.add_widget(self.time_label)
        
        # 启动烟花生成
        Clock.schedule_interval(self.update_fireworks, 1/60.0)
        Clock.schedule_interval(self.add_random_firework, 0.7)
        Clock.schedule_interval(self.update_time, 1)
        
        # 初始烟花
        for i in range(8):
            Clock.schedule_once(lambda dt, idx=i: self.add_random_firework(dt), idx * 0.3)
    
    def get_current_time(self):
        """获取当前时间"""
        now = datetime.now()
        return now.strftime("%Y年%m月%d日 %H:%M:%S")
    
    def update_time(self, dt):
        """更新时间显示"""
        self.time_label.text = self.get_current_time()
    
    def add_random_firework(self, dt=0):
        """添加随机烟花"""
        x = random.randint(100, Window.width - 100)
        y = random.randint(0, 50)
        
        # 节日主题色
        colors = [
            [1, 0, 0, 1],      # 红色 - 喜庆
            [1, 1, 0, 1],      # 黄色 - 辉煌
            [0, 1, 1, 1],      # 青色 - 清新
            [1, 0, 1, 1],      # 紫色 - 浪漫
            [0.2, 0.8, 1, 1],  # 蓝色 - 宁静
            [1, 0.6, 0, 1],    # 橙色 - 温暖
            [0.6, 1, 0.2, 1],  # 绿色 - 生机
            None               # 随机颜色
        ]
        
        color_choice = random.choice(colors)
        
        firework = Firework(x, y, color_choice)
        self.fireworks.append(firework)
        self.add_widget(firework)
        
        # 30%几率添加双发烟花
        if random.random() < 0.3:
            Clock.schedule_once(lambda dt: self.add_random_firework(dt), 0.2)
    
    def update_fireworks(self, dt):
        """更新所有烟花"""
        # 更新烟花状态
        active_fireworks = []
        
        for firework in self.fireworks:
            if firework.update(dt):
                active_fireworks.append(firework)
            else:
                self.remove_widget(firework)
        
        self.fireworks = active_fireworks
        
        # 重绘
        self.canvas.after.clear()
        with self.canvas.after:
            self.draw_fireworks()
    
    def draw_fireworks(self):
        """绘制烟花"""
        for firework in self.fireworks:
            # 绘制轨迹
            if len(firework.trail) > 1:
                trail_color = list(firework.color)
                trail_color[3] = 0.6
                
                Color(*trail_color)
                Line(points=[coord for point in firework.trail for coord in point], 
                     width=2.0)
            
            # 绘制粒子
            for particle in firework.particles:
                Color(*particle.color)
                Ellipse(pos=(particle.x - particle.size/2, 
                            particle.y - particle.size/2),
                       size=(particle.size, particle.size))
                
                # 光晕效果
                if particle.life > 0.5:
                    glow_size = particle.size * 2.5
                    glow_color = list(particle.color)
                    glow_color[3] = particle.color[3] * 0.2
                    
                    Color(*glow_color)
                    Ellipse(pos=(particle.x - glow_size/2, 
                                particle.y - glow_size/2),
                           size=(glow_size, glow_size))
    
    def on_touch_down(self, touch):
        """点击屏幕添加烟花"""
        # 避开文字区域（中央区域不响应点击）
        text_rect = (self.welcome_message.x, self.welcome_message.y,
                    self.welcome_message.width, self.welcome_message.height)
        
        if not (text_rect[0] <= touch.x <= text_rect[0] + text_rect[2] and
                text_rect[1] <= touch.y <= text_rect[1] + text_rect[3]):
            
            firework = Firework(touch.x, touch.y)
            self.fireworks.append(firework)
            self.add_widget(firework)
            
            # 点击特效
            with self.canvas:
                Color(1, 1, 1, 0.3)
                Ellipse(pos=(touch.x - 25, touch.y - 25), size=(50, 50))
                Color(1, 0.8, 0, 0.2)
                Ellipse(pos=(touch.x - 40, touch.y - 40), size=(80, 80))
            
            return True
        return super().on_touch_down(touch)


class WelcomeFireworksApp(App):
    """烟花欢迎应用"""
    
    def build(self):
        self.title = "烟花绽放欢迎效果"
        display = FireworksDisplay()
        Window.bind(on_keyboard=self.on_keyboard)
        return display
    
    def on_keyboard(self, window, key, *args):
        """键盘事件"""
        if key == 27:  # ESC键
            self.stop()
            return True
        elif key == 32:  # 空格键 - 添加多个烟花
            for _ in range(5):
                Clock.schedule_once(
                    lambda dt, w=window: self.root.add_random_firework(dt), 
                    random.random()
                )
            return True
        return False
    
    def on_start(self):
        """应用启动"""
        print("=" * 50)
        print("烟花欢迎应用已启动")
        print("内容：欢迎姜文斌")
        print("操作说明：")
        print("1. 点击屏幕空白处添加烟花")
        print("2. 按空格键添加多个烟花")
        print("3. 按ESC键退出应用")
        print("=" * 50)
    
    def on_stop(self):
        """应用停止"""
        print("烟花欢迎应用已关闭")


# 备用版本 - 不使用外部字体
class SimpleFireworksApp(App):
    """简化版烟花应用（不使用外部字体）"""
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        Window.size = (1000, 700)
        
        root = FloatLayout()
        
        # 中央显示"欢迎姜文斌"
        welcome_label = Label(
            text="欢迎姜文斌",
            font_size=80,
            bold=True,
            color=(1, 1, 1, 1),
            size=(800, 200),
            pos=(100, 300),
            halign='center',
            valign='middle'
        )
        welcome_label.text_size = (800, 200)
        root.add_widget(welcome_label)
        
        # 烟花效果
        fireworks = []
        particles = []
        
        def update(dt):
            # 更新烟花
            for fw in fireworks[:]:
                if not fw['exploded']:
                    fw['x'] += fw['vx']
                    fw['y'] += fw['vy']
                    fw['vy'] -= 0.1
                    
                    if fw['vy'] < 0 or random.random() < 0.02:
                        fw['exploded'] = True
                        explode(fw['x'], fw['y'], fw['color'])
                        fireworks.remove(fw)
            
            # 更新粒子
            for p in particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] -= 0.05
                p['life'] -= 0.015
                p['vx'] *= 0.98
                p['vy'] *= 0.98
                
                if p['life'] <= 0:
                    particles.remove(p)
            
            # 重绘
            root.canvas.after.clear()
            with root.canvas.after:
                # 绘制烟花轨迹
                for fw in fireworks:
                    Color(*fw['color'] + [0.7])
                    Line(points=[fw['x'], fw['y'], fw['x']-fw['vx']*2, fw['y']-fw['vy']*2], width=2)
                    Color(*fw['color'] + [1])
                    Ellipse(pos=(fw['x']-5, fw['y']-5), size=(10, 10))
                
                # 绘制粒子
                for p in particles:
                    alpha = p['life']
                    Color(p['color'][0], p['color'][1], p['color'][2], alpha)
                    Ellipse(pos=(p['x']-p['size']/2, p['y']-p['size']/2), 
                           size=(p['size'], p['size']))
        
        def explode(x, y, color):
            num = random.randint(60, 100)
            for _ in range(num):
                angle = random.uniform(0, 2*math.pi)
                speed = random.uniform(2, 6)
                particles.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'color': color,
                    'size': random.uniform(3, 8),
                    'life': 1.0
                })
        
        def add_firework(dt):
            x = random.randint(100, 900)
            hue = random.random()
            color = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
            fireworks.append({
                'x': x, 'y': 0,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(8, 12),
                'color': color,
                'exploded': False
            })
        
        def on_touch(touch):
            if touch.y < 250 or touch.y > 450:  # 避开文字区域
                hue = random.random()
                color = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
                fireworks.append({
                    'x': touch.x, 'y': touch.y,
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(5, 9),
                    'color': color,
                    'exploded': False
                })
            return True
        
        # 添加动画
        anim = Animation(color=(1, 0.8, 0, 1), duration=2) + \
               Animation(color=(0.8, 0.8, 1, 1), duration=2) + \
               Animation(color=(1, 1, 1, 1), duration=2)
        anim.repeat = True
        anim.start(welcome_label)
        
        # 设置定时器
        Clock.schedule_interval(update, 1/60.0)
        Clock.schedule_interval(add_firework, 0.8)
        Window.bind(on_touch_down=on_touch)
        
        # 初始烟花
        for i in range(6):
            Clock.schedule_once(lambda dt: add_firework(dt), i * 0.3)
        
        return root


if __name__ == '__main__':
    print("启动烟花欢迎应用...")
    print("窗口内容显示: 欢迎姜文斌")
    print()
    
    # 尝试使用完整版本，如果失败则使用简化版本
    try:
        # 创建字体目录
        font_dir = Path(__file__).parent / 'fonts'
        font_dir.mkdir(exist_ok=True)
        
        # 启动应用
        WelcomeFireworksApp().run()
    except Exception as e:
        print(f"完整版本启动失败: {e}")
        print("正在启动简化版本...")
        SimpleFireworksApp().run()
