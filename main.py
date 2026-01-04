# 先配置渲染后端，适配鸿蒙设备（打包APK必备，本地运行也可保留）
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_NO_FILELOG'] = '1'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase  # 新增：导入字体注册类
from random import random, randint, uniform

# 新增：注册自定义字体 msyhbd.ttc（必须在创建Label之前执行）
# 第一个参数：自定义字体名称（后续Label直接引用该名称）
# 第二个参数：字体文件相对路径（基于项目根目录，对应assets/fonts/目录）
LabelBase.register(
    name='MicrosoftYaHeiBold',
    fn_regular='assets/fonts/msyhbd.ttc'
)

# 烟花粒子类，负责单个粒子的运动和绘制
class FireworkParticle:
    def __init__(self, x, y):
        # 粒子初始位置（烟花爆炸中心）
        self.x = x
        self.y = y
        
        # 粒子运动参数（随机方向、速度、生命周期）
        self.angle = uniform(0, 2 * 3.14159)  # 随机运动角度
        self.speed = uniform(2, 5)             # 随机运动速度
        self.life = 1.0                        # 粒子生命周期（1.0为满生命值）
        self.life_decay = uniform(0.01, 0.03)  # 生命值衰减速度
        
        # 粒子颜色（随机暖色调，模拟烟花色彩）
        self.r = random()  # 红
        self.g = random() * 0.7  # 绿（降低亮度，更贴近烟花）
        self.b = random() * 0.5  # 蓝（降低亮度，更贴近烟花）
        
        # 粒子大小
        self.size = uniform(2, 6)
    
    def update(self, dt):
        """更新粒子位置和生命周期"""
        # 根据角度和速度更新位置
        self.x += self.speed * (self.angle ** 0.5) * (1 if self.angle < 3.14 else -1)
        self.y += self.speed * (self.angle ** 0.5)
        
        # 加入重力效果，让粒子下落
        self.speed -= 0.05
        
        # 衰减生命值
        self.life -= self.life_decay
        if self.life < 0:
            self.life = 0
    
    def is_alive(self):
        """判断粒子是否存活"""
        return self.life > 0

# 主布局类，负责烟花效果绘制和文字展示
class FireworkLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(FireworkLayout, self).__init__(**kwargs)
        
        # 1. 添加「你好 姜文斌」文字标签（修改：指定自定义字体）
        self.text_label = Label(
            text="你好 姜文斌",
            font_size=48,  # 文字大小
            color=(1, 1, 1, 1),  # 白色文字
            pos_hint={'center_x': 0.5, 'center_y': 0.8},  # 居中靠上摆放
            bold=True,  # 加粗文字（与msyhbd.ttc粗体叠加，效果更优）
            font_name='MicrosoftYaHeiBold'  # 新增：引用已注册的自定义字体名称
        )
        self.add_widget(self.text_label)
        
        # 2. 初始化烟花粒子列表
        self.firework_particles = []
        
        # 3. 定时触发烟花爆炸（每1.5秒一次）
        Clock.schedule_interval(self.spawn_firework, 1.5)
        
        # 4. 定时更新粒子状态和重绘（每帧更新）
        Clock.schedule_interval(self.update_fireworks, 1/60)
    
    def spawn_firework(self, dt):
        """生成新的烟花（随机位置爆炸）"""
        # 随机选择烟花爆炸中心（窗口内）
        spawn_x = randint(50, int(Window.width) - 50)
        spawn_y = randint(50, int(Window.height) - 200)
        
        # 生成一组烟花粒子（每个烟花包含50-80个粒子）
        particle_count = randint(50, 80)
        for _ in range(particle_count):
            particle = FireworkParticle(spawn_x, spawn_y)
            self.firework_particles.append(particle)
    
    def update_fireworks(self, dt):
        """更新所有粒子状态，并重绘烟花"""
        # 清理画布
        self.canvas.clear()
        
        # 先绘制文字标签的背景（可选，提升文字可读性）
        with self.canvas.before:
            Color(0, 0, 0, 0.3)  # 半透明黑色背景
            Ellipse(
                size=(self.text_label.width + 40, self.text_label.height + 20),
                pos=(
                    self.text_label.x - 20,
                    self.text_label.y - 10
                )
            )
        
        # 更新并绘制所有存活的粒子
        alive_particles = []
        for particle in self.firework_particles:
            particle.update(dt)
            if particle.is_alive():
                alive_particles.append(particle)
                
                # 绘制单个粒子（根据生命值调整透明度）
                with self.canvas:
                    Color(
                        particle.r,
                        particle.g,
                        particle.b,
                        particle.life  # 生命值作为透明度，粒子逐渐消失
                    )
                    Ellipse(
                        size=(particle.size, particle.size),
                        pos=(particle.x, particle.y)
                    )
        
        # 更新粒子列表，仅保留存活的粒子
        self.firework_particles = alive_particles

# 主App类
class FireworkApp(App):
    def build(self):
        # 设置窗口标题和大小（本地运行有效，打包APK后自适应屏幕）
        self.title = "烟花效果 - 你好 姜文斌"
        Window.size = (800, 600)  # 本地运行窗口大小
        Window.clearcolor = (0, 0, 0, 1)  # 黑色背景，凸显烟花效果
        
        return FireworkLayout()

if __name__ == "__main__":
    FireworkApp().run()
