from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Triangle
from kivy.clock import Clock
import random

class ChristmasTree(Widget):
    def __init__(self, **kwargs):
        super(ChristmasTree, self).__init__(**kwargs)
        self.decorations = []  # 存储所有装饰灯，用于后续闪烁更新
        
        # 初始化绘制（监听屏幕尺寸变化，确保适配）
        self.bind(size=self._redraw_tree)  # 屏幕尺寸变化时重新绘制
        self._redraw_tree()  # 首次初始化绘制

        # 启动定时器，实现装饰灯动态闪烁（安卓端适配帧率，0.5秒更新一次）
        Clock.schedule_interval(self._update_decorations, 0.5)

    def _redraw_tree(self, *args):
        """重新绘制圣诞树（适配安卓屏幕尺寸变化，相对坐标计算）"""
        # 清空原有绘制，避免重复叠加
        self.canvas.clear()
        self.decorations.clear()

        # 安卓端：相对屏幕尺寸计算圣诞树位置（始终居中，适配不同手机屏幕）
        self.tree_center_x = self.size[0] / 2  # 基于控件宽度居中（跟随手机屏幕宽度）
        self.tree_bottom_y = self.size[1] * 0.1  # 底部留10%屏幕高度，避免贴近手机底部

        # 1. 绘制圣诞树背景（替代原Window.clearcolor，适配安卓）
        with self.canvas:
            Color(0.05, 0.05, 0.1, 1)  # 深夜空蓝背景
            Rectangle(pos=self.pos, size=self.size)

        # 2. 绘制树干和树体
        self._draw_tree_trunk()
        self._draw_tree_body()
        self._draw_decorations()

    def _draw_tree_trunk(self):
        """绘制圣诞树树干（适配安卓相对尺寸，不硬编码）"""
        # 相对屏幕高度计算树干尺寸，适配不同手机
        trunk_width = self.size[1] * 0.05  # 树干宽度=屏幕高度5%
        trunk_height = self.size[1] * 0.1  # 树干高度=屏幕高度10%
        with self.canvas:
            # 树干棕色
            Color(0.6, 0.3, 0.1, 1)
            Rectangle(
                pos=(self.tree_center_x - trunk_width/2, self.tree_bottom_y),
                size=(trunk_width, trunk_height)
            )

    def _draw_tree_body(self):
        """绘制分层圣诞树主体（适配安卓相对尺寸，3层递进）"""
        # 相对屏幕高度计算树体尺寸，适配不同手机
        base_layer_width = self.size[1] * 0.25  # 最下层宽度=屏幕高度25%
        base_layer_height = self.size[1] * 0.18  # 最下层高度=屏幕高度18%
        
        tree_layers = [
            (base_layer_width, base_layer_height),  # 第一层（最下层）
            (base_layer_width * 0.7, base_layer_height * 0.9),  # 第二层（70%宽度，90%高度）
            (base_layer_width * 0.4, base_layer_height * 0.8)   # 第三层（最上层，40%宽度，80%高度）
        ]
        current_y = self.tree_bottom_y + self.size[1] * 0.1  # 从树干顶部开始绘制第一层

        with self.canvas:
            for layer_width, layer_height in tree_layers:
                # 圣诞树深绿到浅绿渐变，提升层次感
                green_shade = 0.2 + (current_y / self.size[1]) * 0.5
                Color(green_shade, 0.7, 0.2, 1)

                # 计算三角形三个顶点坐标（居中绘制，跟随屏幕尺寸变化）
                p1 = (self.tree_center_x - layer_width/2, current_y)
                p2 = (self.tree_center_x + layer_width/2, current_y)
                p3 = (self.tree_center_x, current_y + layer_height)

                # 绘制三角形分层，构成圣诞树主体
                Triangle(points=[p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]])

                # 更新下一层起始y坐标（叠加当前层高度）
                current_y += layer_height - self.size[1] * 0.02  # 轻微重叠，增强整体感

    def _draw_decorations(self):
        """绘制圣诞树装饰灯（彩色圆形，适配安卓屏幕，随机分布）"""
        decoration_count = 50  # 装饰灯数量（可根据屏幕尺寸调整，此处固定）
        min_y = self.tree_bottom_y + self.size[1] * 0.12
        max_y = self.tree_bottom_y + self.size[1] * 0.45
        max_radius = self.size[1] * 0.01  # 装饰灯最大半径=屏幕高度1%，适配不同手机

        with self.canvas:
            for _ in range(decoration_count):
                # 随机生成装饰灯位置（限制在圣诞树主体范围内，跟随屏幕变化）
                x_offset = random.uniform(-self.size[1]*0.22, self.size[1]*0.22)
                y = random.uniform(min_y, max_y)
                # 越往上，x偏移越小，贴合圣诞树形状
                x = self.tree_center_x + x_offset * (1 - (y - min_y)/(max_y - min_y))
                radius = random.uniform(self.size[1]*0.006, max_radius)

                # 随机生成鲜艳的装饰灯颜色（红、黄、蓝、粉、紫）
                color_choices = [
                    (1, 0, 0, 1),    # 红
                    (1, 1, 0, 1),    # 黄
                    (0, 0, 1, 1),    # 蓝
                    (1, 0.5, 0.8, 1),# 粉
                    (0.7, 0, 1, 1)   # 紫
                ]
                color = random.choice(color_choices)

                # 绘制装饰灯并存储相关信息（用于后续闪烁更新）
                ellipse = Ellipse(
                    pos=(x - radius/2, y - radius/2),
                    size=(radius, radius)
                )
                self.decorations.append({
                    'ellipse': ellipse,
                    'color': color,
                    'radius': radius,
                    'pos': (x, y),
                    'active': random.choice([True, False])  # 初始随机亮灭状态
                })

    def _update_decorations(self, dt):
        """更新装饰灯状态，实现动态闪烁效果（安卓端流畅运行）"""
        # 清空原有装饰灯颜色（重新绘制以更新状态）
        self.canvas.after.clear()

        with self.canvas.after:
            for deco in self.decorations:
                # 随机切换亮灭状态，实现闪烁效果
                if random.random() < 0.2:
                    deco['active'] = not deco['active']

                # 亮灯：显示原颜色；灭灯：显示背景暗色调，模拟熄灭
                if deco['active']:
                    Color(*deco['color'])
                else:
                    Color(0.05, 0.05, 0.1, 1)  # 与背景色一致，隐藏装饰灯

                # 重新绘制装饰灯（更新亮灭状态，适配屏幕尺寸）
                Ellipse(
                    pos=(deco['pos'][0] - deco['radius']/2, deco['pos'][1] - deco['radius']/2),
                    size=(deco['radius'], deco['radius'])
                )

class ChristmasTreeApp(App):
    def build(self):
        self.title = "文斌工作室 - 圣诞树"  # 安卓端APP窗口标题（部分手机显示在状态栏）
        return ChristmasTree()

    def on_pause(self):
        """安卓端专属：处理应用暂停（如按Home键），返回True支持恢复"""
        return True

    def on_resume(self):
        """安卓端专属：处理应用恢复，重新启动定时器（可选，确保闪烁效果不中断）"""
        pass

if __name__ == '__main__':
    ChristmasTreeApp().run()
