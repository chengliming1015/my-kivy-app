from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock, mainthread
from kivy.utils import platform
import os

# 只针对Android平台
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    try:
        from plyer import gps
        PLYER_AVAILABLE = True
    except ImportError:
        PLYER_AVAILABLE = False
else:
    PLYER_AVAILABLE = False

class SimpleGPSApp(App):
    # 字体路径
    FONT_PATH = 'fonts/msyhbd.ttc'
    
    def build(self):
        # 检查字体文件是否存在
        if os.path.exists(self.FONT_PATH):
            from kivy.core.text import LabelBase
            # 注册字体
            LabelBase.register(name='MicrosoftYaHeiBold', 
                             fn_regular=self.FONT_PATH)
            self.font_name = 'MicrosoftYaHeiBold'
        else:
            print(f"字体文件不存在: {self.FONT_PATH}")
            self.font_name = 'Roboto'  # 使用默认字体
        
        # 设置主题颜色
        from kivy.core.window import Window
        Window.clearcolor = (0.05, 0.1, 0.15, 1)  # 深色背景
        
        return GPSLayout(font_name=self.font_name)
    
    def on_start(self):
        # 应用启动时请求权限
        if platform == 'android':
            self.request_android_permissions()
    
    def request_android_permissions(self):
        """请求Android权限"""
        try:
            required_permissions = [
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
            ]
            
            def permission_callback(permissions, results):
                if all(results):
                    print("权限已授予")
                else:
                    print("部分权限被拒绝")
                    
            request_permissions(required_permissions, permission_callback)
            
        except Exception as e:
            print(f"权限请求失败: {e}")

class GPSLayout(BoxLayout):
    def __init__(self, font_name='Roboto', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 15
        
        # 保存字体名称
        self.font_name = font_name
        
        # GPS状态
        self.gps_started = False
        self.last_location = None
        
        # 创建UI
        self.create_ui()
        
    def create_ui(self):
        """创建简洁的UI界面"""
        # 标题
        title = Label(
            text='Android GPS定位',
            font_size=28,
            font_name=self.font_name,
            bold=True,
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.2)
        )
        
        # 状态显示
        self.status_label = Label(
            text='准备中...',
            font_size=18,
            font_name=self.font_name,
            color=(1, 1, 1, 0.8),
            size_hint=(1, 0.1)
        )
        
        # 纬度显示
        lat_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        lat_title = Label(
            text='纬度:',
            font_size=20,
            font_name=self.font_name,
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(0.3, 1),
            halign='right'
        )
        self.lat_label = Label(
            text='0.000000°',
            font_size=22,
            font_name=self.font_name,
            bold=True,
            color=(0.2, 0.9, 0.5, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        lat_box.add_widget(lat_title)
        lat_box.add_widget(self.lat_label)
        
        # 经度显示
        lon_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        lon_title = Label(
            text='经度:',
            font_size=20,
            font_name=self.font_name,
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(0.3, 1),
            halign='right'
        )
        self.lon_label = Label(
            text='0.000000°',
            font_size=22,
            font_name=self.font_name,
            bold=True,
            color=(0.2, 0.9, 0.5, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        lon_box.add_widget(lon_title)
        lon_box.add_widget(self.lon_label)
        
        # 精度显示
        acc_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        acc_title = Label(
            text='精度:',
            font_size=20,
            font_name=self.font_name,
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(0.3, 1),
            halign='right'
        )
        self.acc_label = Label(
            text='0.0米',
            font_size=22,
            font_name=self.font_name,
            bold=True,
            color=(1, 0.8, 0.2, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        acc_box.add_widget(acc_title)
        acc_box.add_widget(self.acc_label)
        
        # 卫星数显示
        sat_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        sat_title = Label(
            text='卫星:',
            font_size=20,
            font_name=self.font_name,
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(0.3, 1),
            halign='right'
        )
        self.sat_label = Label(
            text='0',
            font_size=22,
            font_name=self.font_name,
            bold=True,
            color=(0.8, 0.6, 1, 1),
            size_hint=(0.7, 1),
            halign='left'
        )
        sat_box.add_widget(sat_title)
        sat_box.add_widget(self.sat_label)
        
        # 控制按钮
        btn_box = BoxLayout(size_hint=(1, 0.2), spacing=20)
        
        self.start_btn = Button(
            text='开始定位',
            font_size=24,
            font_name=self.font_name,
            background_color=(0.2, 0.6, 0.9, 1),
            size_hint=(0.5, 1)
        )
        self.start_btn.bind(on_press=self.toggle_gps)
        
        self.refresh_btn = Button(
            text='刷新',
            font_size=24,
            font_name=self.font_name,
            background_color=(0.3, 0.5, 0.7, 1),
            size_hint=(0.5, 1)
        )
        self.refresh_btn.bind(on_press=self.refresh_status)
        
        btn_box.add_widget(self.start_btn)
        btn_box.add_widget(self.refresh_btn)
        
        # 组装所有组件
        self.add_widget(title)
        self.add_widget(self.status_label)
        self.add_widget(lat_box)
        self.add_widget(lon_box)
        self.add_widget(acc_box)
        self.add_widget(sat_box)
        self.add_widget(btn_box)
        
        # 添加空白区域
        spacer = Label(text='', size_hint=(1, 0.05))
        self.add_widget(spacer)
        
        # 延迟启动GPS（等待权限请求完成）
        Clock.schedule_once(self.delayed_init, 2)
    
    def delayed_init(self, dt):
        """延迟初始化"""
        if platform == 'android' and PLYER_AVAILABLE:
            self.init_gps()
        else:
            self.update_status("不支持GPS或plyer不可用", is_error=True)
    
    def init_gps(self):
        """初始化GPS"""
        try:
            # 配置GPS回调
            gps.configure(
                on_location=self.on_gps_location,
                on_status=self.on_gps_status
            )
            self.update_status("GPS已初始化")
            
        except Exception as e:
            self.update_status(f"GPS初始化失败: {str(e)}", is_error=True)
    
    def toggle_gps(self, instance):
        """切换GPS状态"""
        if not PLYER_AVAILABLE:
            self.update_status("GPS模块不可用", is_error=True)
            return
            
        if self.gps_started:
            self.stop_gps()
            instance.text = "开始定位"
            instance.background_color = (0.2, 0.6, 0.9, 1)
        else:
            self.start_gps()
            instance.text = "停止定位"
            instance.background_color = (0.9, 0.3, 0.3, 1)
    
    def start_gps(self):
        """启动GPS"""
        try:
            gps.start(
                minTime=1000,       # 1秒更新一次
                minDistance=1,      # 移动1米更新
                preferredAccuracy=10 # 首选10米精度
            )
            self.gps_started = True
            self.update_status("GPS已启动，搜索卫星中...")
            
        except Exception as e:
            self.update_status(f"GPS启动失败: {str(e)}", is_error=True)
    
    def stop_gps(self):
        """停止GPS"""
        try:
            if self.gps_started:
                gps.stop()
                self.gps_started = False
                self.update_status("GPS已停止")
                
        except Exception as e:
            self.update_status(f"GPS停止失败: {str(e)}", is_error=True)
    
    @mainthread
    def on_gps_location(self, **kwargs):
        """GPS位置更新回调"""
        try:
            # 获取数据
            lat = kwargs.get('lat', 0)
            lon = kwargs.get('lon', 0)
            accuracy = kwargs.get('accuracy', kwargs.get('gps_accuracy', 0))
            satellites = kwargs.get('satellites', kwargs.get('num_satellites', 0))
            
            # 更新UI
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                self.lat_label.text = f"{lat:.6f}°"
                self.lon_label.text = f"{lon:.6f}°"
            else:
                self.lat_label.text = str(lat)
                self.lon_label.text = str(lon)
            
            self.acc_label.text = f"{accuracy:.1f}米"
            self.sat_label.text = str(satellites)
            
            # 更新状态
            if satellites > 0:
                self.update_status(f"定位成功 ({satellites}颗卫星)")
            else:
                self.update_status("定位中...")
            
            # 保存最后位置
            self.last_location = (lat, lon)
            
        except Exception as e:
            print(f"位置数据处理错误: {e}")
    
    @mainthread
    def on_gps_status(self, stype, status):
        """GPS状态回调"""
        status_messages = {
            'provider-enabled': '定位服务已启用',
            'provider-disabled': '定位服务已禁用',
            'gps-status': f'GPS状态: {status}',
            'started': 'GPS已启动',
            'stopped': 'GPS已停止'
        }
        
        message = status_messages.get(stype, f"状态更新: {stype}")
        self.update_status(f"{message}")
    
    @mainthread
    def update_status(self, text, is_error=False):
        """更新状态显示"""
        if is_error:
            self.status_label.color = (1, 0.3, 0.3, 1)  # 红色错误
        else:
            self.status_label.color = (0.2, 0.8, 0.3, 1)  # 绿色正常
        
        self.status_label.text = text
    
    def refresh_status(self, instance):
        """刷新状态"""
        if self.last_location:
            lat, lon = self.last_location
            self.update_status(f"最后位置: {lat:.6f}, {lon:.6f}")
        else:
            self.update_status("等待定位数据...")
    
    def on_stop(self):
        """停止应用时停止GPS"""
        self.stop_gps()

if __name__ == '__main__':
    # 检查是否在Android平台
    if platform != 'android':
        print("警告: 此应用专为Android平台设计")
        print("在非Android平台上，GPS功能可能无法正常工作")
    
    # 运行应用
    SimpleGPSApp().run()
