# 解决PyCharm警告的优化版本
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.clock import Clock
import os
import itertools

# 检查字体文件是否存在
FONT_PATH = "fonts/simhei.ttf"  # 'simhei' 是字体名称，无需修改
if not os.path.exists(FONT_PATH):
    print(f"警告: 字体文件 '{FONT_PATH}' 不存在，将使用默认字体")


class CustomLabel(Label):
    """自定义标签，使用指定字体"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_PATH if os.path.exists(FONT_PATH) else None


class CustomButton(Button):
    """自定义按钮，使用指定字体"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_PATH if os.path.exists(FONT_PATH) else None


class CustomTextInput(TextInput):
    """自定义文本输入，使用指定字体"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_PATH if os.path.exists(FONT_PATH) else None


class CustomSpinner(Spinner):
    """自定义下拉选择器，使用指定字体"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_PATH if os.path.exists(FONT_PATH) else None


class PasswordDigit(BoxLayout):
    """单个密码数字显示框 - 蓝色立体球形"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(70), dp(70))  # 增大尺寸以适应球形效果
        self.padding = dp(5)
        
        # 绘制蓝色立体球形
        self._create_sphere_graphics()
        
        # 数字标签
        self.label = CustomLabel(
            text="?",
            font_size=sp(34),
            color=(1, 1, 1, 1),  # 白色
            bold=True,
            outline_width=dp(1),
            outline_color=(0.2, 0.3, 0.5, 1)  # 深蓝色轮廓
        )
        self.add_widget(self.label)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
    
    def _create_sphere_graphics(self):
        """创建球形图形元素"""
        with self.canvas.before:
            # 清除之前的绘制
            self.canvas.before.clear()
            
            # 基础蓝色球体
            Color(0.3, 0.5, 0.8, 1)  # 深蓝色
            self.ellipse = Ellipse(
                size=(dp(65), dp(65)),  # 稍小于容器大小
                pos=(self.pos[0] + dp(2.5), self.pos[1] + dp(2.5))  # 居中
            )
            
            # 球体高光（左上角）
            Color(0.5, 0.7, 1, 0.8)  # 浅蓝色高光
            self.highlight = Ellipse(
                size=(dp(25), dp(25)),
                pos=(self.pos[0] + dp(10), self.pos[1] + dp(40))  # 左上角
            )
            
            # 球体阴影（右下角）
            Color(0.2, 0.4, 0.7, 0.6)  # 深蓝色阴影
            self.shadow = Ellipse(
                size=(dp(20), dp(20)),
                pos=(self.pos[0] + dp(45), self.pos[1] + dp(5))  # 右下角
            )
            
            # 球体边缘光晕
            Color(0.4, 0.6, 0.9, 0.3)  # 浅蓝色光晕
            self.glow = Ellipse(
                size=(dp(68), dp(68)),
                pos=(self.pos[0] + dp(1), self.pos[1] + dp(1))  # 稍微超出基础球体
            )

    def update_graphics(self, *_args):
        """更新图形位置和大小"""
        # 更新基础球体
        self.ellipse.pos = (self.pos[0] + dp(2.5), self.pos[1] + dp(2.5))
        self.ellipse.size = (dp(65), dp(65))
        
        # 更新高光
        self.highlight.pos = (self.pos[0] + dp(10), self.pos[1] + dp(40))
        self.highlight.size = (dp(25), dp(25))
        
        # 更新阴影
        self.shadow.pos = (self.pos[0] + dp(45), self.pos[1] + dp(5))
        self.shadow.size = (dp(20), dp(20))
        
        # 更新光晕
        self.glow.pos = (self.pos[0] + dp(1), self.pos[1] + dp(1))
        self.glow.size = (dp(68), dp(68))
    
    def set_digit(self, digit):
        """设置数字并更新球体颜色"""
        self.label.text = str(digit)
        
        # 根据数字更新球体颜色（可选，保持蓝色）
        # 这里我们可以根据数字的不同添加微妙的颜色变化
        if digit in ['0', '1', '2', '3']:
            # 冷色调蓝
            with self.canvas.before:
                self.canvas.before.clear()
                Color(0.3, 0.5, 0.8, 1)
                self.ellipse = Ellipse(
                    size=(dp(65), dp(65)),
                    pos=(self.pos[0] + dp(2.5), self.pos[1] + dp(2.5))
                )
        else:
            # 暖色调蓝
            with self.canvas.before:
                self.canvas.before.clear()
                Color(0.3, 0.6, 0.9, 1)
                self.ellipse = Ellipse(
                    size=(dp(65), dp(65)),
                    pos=(self.pos[0] + dp(2.5), self.pos[1] + dp(2.5))
                )
        
        # 重新添加高光和阴影
        self._create_sphere_graphics()


class PasswordDisplay(BoxLayout):
    """密码显示区域 - 蓝色立体球形"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(120)  # 增加高度以适应球形
        self.spacing = dp(15)  # 增加间距
        self.padding = [dp(20), dp(20)]

        # 创建4个蓝色立体球形数字显示框
        self.digit_widgets = []
        for i in range(4):
            digit_widget = PasswordDigit()
            self.digit_widgets.append(digit_widget)
            self.add_widget(digit_widget)

    def set_password(self, password):
        """设置密码显示"""
        for i in range(4):
            if i < len(password):
                self.digit_widgets[i].set_digit(password[i])
            else:
                self.digit_widgets[i].set_digit("?")


class ConditionInputRow(GridLayout):
    """单个条件输入行"""

    def __init__(self, condition_num=1, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 1
        self.size_hint = (1, None)
        self.height = dp(60)
        self.spacing = dp(5)
        self.padding = [0, dp(5)]

        # 条件序号标签
        condition_label = CustomLabel(
            text=f"{condition_num}.",
            size_hint_x=0.12,
            font_size=sp(18),
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            valign='middle'
        )
        condition_label.bind(size=condition_label.setter('text_size'))
        self.add_widget(condition_label)

        # 密码输入框
        self.password_input = CustomTextInput(
            text="",
            multiline=False,
            size_hint_x=0.35,
            font_size=sp(20),
            halign='center',
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.2, 0.2, 0.2, 1),
            padding=[dp(10), dp(10)],
            write_tab=False
        )
        self.add_widget(self.password_input)

        # 号码出现次数选择器
        self.digit_spinner = CustomSpinner(
            text='0',
            values=['0', '1', '2', '3', '4'],
            size_hint_x=0.24,
            font_size=sp(18),
            background_color=(0.85, 0.85, 0.9, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.add_widget(self.digit_spinner)

        # 位置正确个数选择器
        self.position_spinner = CustomSpinner(
            text='0',
            values=['0', '1', '2', '3', '4'],
            size_hint_x=0.24,
            font_size=sp(18),
            background_color=(0.85, 0.85, 0.9, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        self.add_widget(self.position_spinner)


class ConditionInputArea(BoxLayout):
    """条件输入区域 - 5个条件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(350)
        self.spacing = dp(5)
        self.padding = [dp(8), dp(8)]

        # 移除了表头，直接添加5个条件输入行
        self.condition_rows = []
        for i in range(5):
            row = ConditionInputRow(condition_num=i + 1)
            self.condition_rows.append(row)
            self.add_widget(row)


class ActionButtons(BoxLayout):
    """按钮区域"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(60)
        self.spacing = dp(12)
        self.padding = [dp(15), 0]

        # 求解按钮
        self.solve_button = CustomButton(
            text="求解密码",
            font_size=sp(20),
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )

        # 清空按钮
        self.clear_button = CustomButton(
            text="清空重置",
            font_size=sp(20),
            background_color=(0.8, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )

        self.add_widget(self.solve_button)
        self.add_widget(self.clear_button)


class MessageDisplay(BoxLayout):
    """消息显示区域"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(80)  # 增加高度以容纳更多信息
        self.spacing = dp(5)
        self.padding = [dp(15), dp(8)]

        # 主消息标签
        self.main_label = CustomLabel(
            text="等待操作...",
            size_hint=(1, 0.6),
            font_size=sp(16),
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='middle'
        )
        self.main_label.bind(size=self.main_label.setter('text_size'))
        self.add_widget(self.main_label)

        # 导航按钮区域（初始隐藏）
        self.nav_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.4),
            spacing=dp(4)
        )

        self.prev_button = CustomButton(
            text="<",
            font_size=sp(18),
            size_hint_x=0.5,
            background_color=(0.4, 0.4, 0.6, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )

        self.next_button = CustomButton(
            text=">",
            font_size=sp(18),
            size_hint_x=0.5,
            background_color=(0.4, 0.4, 0.6, 1),
            color=(1, 1, 1, 1),
            background_normal=''
        )

        self.nav_layout.add_widget(self.prev_button)
        self.nav_layout.add_widget(self.next_button)
        self.add_widget(self.nav_layout)

        # 初始隐藏导航按钮
        self.nav_layout.opacity = 0

    def show_info(self, message, color=None):
        """显示信息"""
        self.main_label.text = message
        if color:
            self.main_label.color = color
        else:
            self.main_label.color = (0.2, 0.2, 0.2, 1)

    def show_error(self, message):
        """显示错误信息"""
        self.main_label.text = message
        self.main_label.color = (0.8, 0.2, 0.2, 1)

    def show_solution(self, message):
        """显示解决方案信息"""
        self.main_label.text = message
        self.main_label.color = (0.2, 0.6, 0.2, 1)

    def clear_message(self):
        """清除消息"""
        self.main_label.text = ""
        self.main_label.color = (0.2, 0.2, 0.2, 1)


class AdaptiveLockPickingApp(BoxLayout):
    """自适应全屏主应用界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 初始化所有实例属性
        self.password_display = None
        self.scroll_view = None
        self.condition_area = None
        self.message_display = None
        self.action_buttons = None
        self.solutions = []
        self.current_solution_index = 0
        
        self.orientation = 'vertical'
        self.padding = [dp(10), dp(10)]
        self.spacing = dp(10)

        # 设置窗口背景色为奶白色
        # 'clearcolor' 是Kivy的正确属性名，不是拼写错误
        Window.clearcolor = (0.98, 0.96, 0.92, 1)  # 奶白色

        # 构建自适应布局
        self.build_adaptive_layout()

        # 设置示例条件
        Clock.schedule_once(self.set_example_conditions, 0.1)

        # 绑定窗口大小变化事件
        Window.bind(on_resize=self.on_window_resize)

    def build_adaptive_layout(self):
        """构建自适应布局"""
        # 清空现有组件
        self.clear_widgets()

        # 标题区域
        title_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(90),
            spacing=dp(3)
        )

        # 主标题
        title_label = CustomLabel(
            text="开锁大神",
            font_size=sp(42),
            color=(0.8, 0.4, 0, 1),
            bold=True
        )
        title_box.add_widget(title_label)

        # 副标题 - 文斌工作室
        subtitle_label = CustomLabel(
            text="文斌工作室",
            font_size=sp(20),
            color=(0.4, 0.6, 0.8, 1),
            italic=True
        )
        title_box.add_widget(subtitle_label)

        self.add_widget(title_box)

        # 密码显示 - 蓝色立体球形
        self.password_display = PasswordDisplay()
        self.add_widget(self.password_display)

        # 条件输入区域 - 使用自适应高度的ScrollView
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.condition_area = ConditionInputArea()
        self.scroll_view.add_widget(self.condition_area)
        self.add_widget(self.scroll_view)

        # 消息显示区域
        self.message_display = MessageDisplay()
        self.message_display.prev_button.bind(on_press=self.prev_solution)
        self.message_display.next_button.bind(on_press=self.next_solution)
        self.add_widget(self.message_display)

        # 按钮区域
        self.action_buttons = ActionButtons()
        self.action_buttons.solve_button.bind(on_press=self.solve_password)
        self.action_buttons.clear_button.bind(on_press=self.clear_all)
        self.add_widget(self.action_buttons)

    def on_window_resize(self, window, width, height):
        """窗口大小变化时的回调函数"""
        # 使用下划线表示未使用的参数
        del window, width, height  # 明确标记未使用的参数
        Clock.schedule_once(self._update_layout_callback, 0.1)
    
    def _update_layout_callback(self, dt):
        """更新布局的回调函数"""
        del dt  # 明确标记未使用的参数
        self.update_layout()

    def update_layout(self):
        """更新布局以适应新窗口大小"""
        # 这里可以添加根据窗口大小调整的代码
        pass

    def set_example_conditions(self, dt):
        """设置示例条件"""
        del dt  # 明确标记未使用的参数
        example_conditions = [
            ("4501", "2", "2"),
            ("4896", "2", "1"),
            ("7623", "2", "0"),
            ("0123", "0", "0"),
            ("", "0", "0")
        ]

        for i, (password, digit_count, position_count) in enumerate(example_conditions):
            if i < len(self.condition_area.condition_rows):
                row = self.condition_area.condition_rows[i]
                row.password_input.text = password
                row.digit_spinner.text = digit_count
                row.position_spinner.text = position_count

    def clear_all(self, instance):
        """清空所有输入和显示"""
        del instance  # 明确标记未使用的参数
        for row in self.condition_area.condition_rows:
            row.password_input.text = ""
            row.digit_spinner.text = "0"
            row.position_spinner.text = "0"

        self.password_display.set_password("????")
        self.message_display.nav_layout.opacity = 0
        self.message_display.show_info("已清空，请重新输入条件")
        self.solutions = []
        self.current_solution_index = 0

    @staticmethod
    def check_condition(candidate, condition_num, correct_digits, correct_positions):
        """检查候选数字是否满足条件"""
        candidate_str = str(candidate)
        condition_str = str(condition_num)

        # 计算位置正确的数字
        position_correct = sum(1 for i in range(4)
                               if candidate_str[i] == condition_str[i])

        # 计算数字正确但位置不对的
        digit_correct = 0
        used_candidate = [False] * 4
        used_condition = [False] * 4

        # 先标记位置正确的
        for i in range(4):
            if candidate_str[i] == condition_str[i]:
                used_candidate[i] = True
                used_condition[i] = True

        # 再找数字正确但位置不对的
        for i in range(4):
            if not used_candidate[i]:
                for j in range(4):
                    if not used_condition[j] and candidate_str[i] == condition_str[j]:
                        digit_correct += 1
                        used_candidate[i] = True
                        used_condition[j] = True
                        break

        total_correct = position_correct + digit_correct

        return (total_correct == correct_digits and
                position_correct == correct_positions)

    @staticmethod
    def generate_candidates():
        """生成所有可能的4位密码（数字不重复）"""
        digits = '0123456789'
        candidates = []
        
        for perm in itertools.permutations(digits, 4):
            candidate = ''.join(perm)
            candidates.append(candidate)
        
        return candidates

    def solve_password(self, instance):
        """求解密码 - 支持5个条件，空条件自动跳过"""
        del instance  # 明确标记未使用的参数
        
        # 收集所有条件
        conditions = []
        condition_texts = []

        for i, row in enumerate(self.condition_area.condition_rows):
            password = row.password_input.text.strip()
            digit_count = row.digit_spinner.text
            position_count = row.position_spinner.text

            # 如果密码为空，则跳过这个条件
            if not password:
                continue

            # 验证输入
            if len(password) != 4 or not password.isdigit():
                self.message_display.show_error(f"条件{i + 1}: 密码必须是4位数字")
                return

            try:
                digit_count_int = int(digit_count)
                position_count_int = int(position_count)

                if digit_count_int < 0 or digit_count_int > 4:
                    self.message_display.show_error(f"条件{i + 1}: 号码出现次数必须在0-4之间")
                    return

                if position_count_int < 0 or position_count_int > 4:
                    self.message_display.show_error(f"条件{i + 1}: 位置正确个数必须在0-4之间")
                    return

                if position_count_int > digit_count_int:
                    self.message_display.show_error(f"条件{i + 1}: 位置正确个数不能大于号码出现次数")
                    return

            except ValueError:
                self.message_display.show_error(f"条件{i + 1}: 请输入有效的数字")
                return

            conditions.append((password, digit_count_int, position_count_int))
            condition_texts.append(
                f"请输入[密码{password}] [数字正确{digit_count_int}个] [位置正确{position_count_int}个]")

        # 如果没有输入任何有效条件
        if not conditions:
            self.message_display.show_error("请输入[密码xxxx] [数字正确x个] [位置正确x个]")
            return

        # 显示所有条件文本
        if condition_texts:
            all_conditions_text = "\n".join(condition_texts)
            self.message_display.show_info(all_conditions_text)

        # 隐藏导航按钮（等待求解结果）
        self.message_display.nav_layout.opacity = 0

        # 求解过程
        self.solutions = []

        # 生成所有可能的4位数字（数字不重复）
        candidates = self.generate_candidates()
        
        # 统计信息
        total_candidates = len(candidates)
        print(f"生成 {total_candidates} 个候选密码（数字不重复）")

        # 检查每个候选密码
        for candidate in candidates:
            match_all = True

            for password, digit_count, position_count in conditions:
                if not self.check_condition(candidate, password, digit_count, position_count):
                    match_all = False
                    break

            if match_all:
                self.solutions.append(candidate)

        # 显示结果
        if self.solutions:
            self.current_solution_index = 0
            self.show_solution(self.current_solution_index)
        else:
            self.password_display.set_password("????")
            self.message_display.show_solution(f"未找到符合条件的密码（检查了{total_candidates}个候选密码）")
            self.message_display.nav_layout.opacity = 0

    def show_solution(self, index):
        """显示指定索引的解决方案"""
        if index < len(self.solutions):
            solution = self.solutions[index]
            self.password_display.set_password(solution)

            if len(self.solutions) == 1:
                self.message_display.show_solution(f"唯一解: {solution}")
                self.message_display.nav_layout.opacity = 0
            else:
                self.message_display.show_solution(f"解 {index + 1}/{len(self.solutions)}: {solution}")
                self.message_display.nav_layout.opacity = 1

    def prev_solution(self, instance):
        """显示上一个解"""
        del instance  # 明确标记未使用的参数
        if self.solutions and len(self.solutions) > 1:
            self.current_solution_index = (self.current_solution_index - 1) % len(self.solutions)
            self.show_solution(self.current_solution_index)

    def next_solution(self, instance):
        """显示下一个解"""
        del instance  # 明确标记未使用的参数
        if self.solutions and len(self.solutions) > 1:
            self.current_solution_index = (self.current_solution_index + 1) % len(self.solutions)
            self.show_solution(self.current_solution_index)


class LockPickingMasterAdaptiveApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "开锁大神"

    def build(self):
        # 检查字体文件并显示状态
        if os.path.exists(FONT_PATH):
            print(f"✓ 成功加载字体文件: {FONT_PATH}")
        else:
            print(f"✗ 字体文件未找到: {FONT_PATH}，将使用默认字体")

        # 创建自适应应用
        return AdaptiveLockPickingApp()


if __name__ == '__main__':
    LockPickingMasterAdaptiveApp().run()
