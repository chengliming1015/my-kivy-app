from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
import random
import math

# 粒子类：管理烟花爆炸后的单个粒子
class Particle:
    def __init__(self, x, y):
        # 粒子初始位置（烟花爆炸中心）
        self.x = x
        self.y = y
        
        # 随机生成粒子爆炸方向（0-360度）
        angle = random.uniform(0, 2 * math.pi)
        # 随机生成粒子爆炸速度
        speed = random.uniform(2, 5)
        
        # 分解为x、y方向的速度
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # 随机生成烟花颜色（暖色调为主，也可自定义）
        self.r = random.uniform(0.8, 1.0)  # 红
        self.g = random.uniform(0.2, 0.9)  # 绿
        self.b = random.uniform(0.0, 0.8)  # 蓝
        self.a = 1.0  # 透明度（逐渐衰减）
        
        # 粒子生命周期（帧数）
        self.life = random.randint(30, 60)
        # 粒子大小
        self.size = random.uniform(2, 4)
        
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

# 烟花类：管理单个烟花的爆炸和粒子集合
class Firework:
    def __init__(self):
        # 随机生成烟花爆炸位置（在窗口内）
        self.x = random.uniform(Window.width * 0.2, Window.width * 0.8)
        self.y = random.uniform(Window.height * 0.3, Window.height * 0.7)
        
        # 生成烟花粒子集合（单个烟花包含50-100个粒子）
        self.particles = [Particle(self.x, self.y) for _ in range(random.randint(50, 100))]
    
    def update(self):
        """更新所有粒子的状态，返回是否还有存活粒子"""
        for particle in self.particles:
            particle.update()
        
        # 过滤掉生命周期结束的粒子
        self.particles = [p for p in self.particles if p.life > 0]
        
        # 返回是否还有存活粒子（无存活则烟花消失）
        return len(self.particles) > 0

# 烟花画布：负责绘制和管理所有烟花
class FireworkCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 烟花集合
        self.fireworks = []
        
        # 定时刷新动画（60帧/秒）
        Clock.schedule_interval(self.update, 1/60)
        
        # 定时生成新烟花（每0.5-1秒生成一个）
        self.schedule_new_firework()
    
    def schedule_new_firework(self):
        """定时生成新烟花，递归调用实现持续生成"""
        self.add_firework()
        # 随机间隔（500-1000毫秒）生成下一个烟花
        Clock.schedule_once(lambda dt: self.schedule_new_firework(), random.uniform(0.5, 1.0))
    
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
                    pos=(particle.x - particle.size/2, particle.y - particle.size/2),
                    size=(particle.size, particle.size)
                )

# 烟花应用主类
class FireworkApp(App):
    def build(self):
        # 设置窗口大小
        Window.size = (800, 600)
        # 设置窗口标题
        self.title = "Kivy 烟花效果演示"
        # 返回烟花画布
        return FireworkCanvas()

if __name__ == "__main__":
    FireworkApp().run()
