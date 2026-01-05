from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import mainthread, Clock
from kivy.utils import platform
import threading

# 平台特定的GPS导入
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from jnius import autoclass

# 尝试导入plyer
try:
    from plyer import gps
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


class LocationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(LocationLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        
        # 背景设置
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 标题
        self.title_label = Label(
            text="📱 实时定位应用",
            font_size=28,
            bold=True,
            color=(0.9, 0.9, 0.9, 1)
        )
        
        # 状态信息
        self.status_label = Label(
            text="正在初始化...",
            font_size=16,
            color=(1, 0.8, 0.4, 1)
        )
        
        # 定位信息
        self.info_label = Label(
            text="等待定位数据...",
            font_size=18,
            color=(0.6, 0.9, 1.0, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.6)
        )
        self.info_label.bind(size=self._update_text_size)
        
        # 提示信息
        self.tips_label = Label(
            text="请确保已开启GPS定位\n首次使用需要位置权限",
            font_size=14,
            color=(0.8, 0.8, 0.8, 0.8),
            italic=True
        )
        
        self.add_widget(self.title_label)
        self.add_widget(self.status_label)
        self.add_widget(self.info_label)
        self.add_widget(self.tips_label)
        
        # 延迟初始化
        Clock.schedule_once(self._init_app, 1)
    
    def _update_text_size(self, instance, size):
        instance.text_size = size
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def _init_app(self, dt):
        """初始化应用"""
        if platform == 'android':
            self._check_android_permissions()
        else:
            self._init_gps()
    
    def _check_android_permissions(self):
        """检查并请求Android权限"""
        try:
            from android.permissions import request_permissions, Permission
            
            permissions = [
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.INTERNET
            ]
            
            def callback(permissions, grant_results):
                if all(grant_results):
                    self.update_status("权限已获取，启动GPS...")
                    self._init_gps()
                else:
                    self.update_status("权限被拒绝，无法定位")
                    self.update_info("请在设置中授予位置权限")
            
            request_permissions(permissions, callback)
            
        except ImportError:
            # 非Android平台
            self._init_gps()
        except Exception as e:
            self.update_status(f"权限检查失败: {str(e)}")
            self._init_gps()
    
    def _init_gps(self):
        """初始化GPS"""
        if not PLYER_AVAILABLE:
            self.update_status("GPS模块不可用")
            self._show_test_data()
            return
        
        try:
            from plyer import gps
            
            # 配置GPS回调
            gps.configure(
                on_location=self.on_location,
                on_status=self.on_status
            )
            
            # 启动GPS
            gps.start(minTime=1000, minDistance=1)
            self.update_status("GPS服务已启动")
            
        except NotImplementedError:
            self.update_status("当前平台不支持GPS")
            self._show_test_data()
        except Exception as e:
            self.update_status(f"GPS启动失败: {str(e)}")
            self._show_test_data()
    
    def _show_test_data(self):
        """显示测试数据"""
        test_data = {
            'lat': 31.2304,
            'lon': 121.4737,
            'alt': 5.0,
            'speed': 0.0
        }
        self.on_location(**test_data)
    
    @mainthread
    def on_location(self, **kwargs):
        """位置更新回调"""
        try:
            lat = kwargs.get('lat', 0)
            lon = kwargs.get('lon', 0)
            alt = kwargs.get('alt', kwargs.get('altitude', 0))
            speed = kwargs.get('speed', 0)
            
            # 格式化为字符串
            if isinstance(lat, (int, float)):
                lat_str = f"{lat:.6f}°"
            else:
                lat_str = str(lat)
            
            if isinstance(lon, (int, float)):
                lon_str = f"{lon:.6f}°"
            else:
                lon_str = str(lon)
            
            info_text = (
                f"📍 位置信息\n\n"
                f"纬度: {lat_str}\n"
                f"经度: {lon_str}\n"
                f"海拔: {alt:.1f}米\n"
                f"速度: {speed:.1f}m/s\n\n"
                f"更新时间: {Clock.get_strftime()}"
            )
            
            self.update_status("定位成功 ✓")
            self.update_info(info_text)
            
        except Exception as e:
            self.update_status(f"数据错误: {str(e)}")
    
    @mainthread
    def on_status(self, stype, status):
        """GPS状态回调"""
        status_map = {
            'provider-enabled': '定位服务已启用',
            'provider-disabled': '定位服务已禁用',
            'started': 'GPS已启动',
            'stopped': 'GPS已停止'
        }
        
        message = status_map.get(stype, f"状态: {stype}")
        self.update_status(f"{message} - {status}")
    
    @mainthread
    def update_status(self, text):
        self.status_label.text = f"状态: {text}"
    
    @mainthread
    def update_info(self, text):
        self.info_label.text = text
    
    def stop(self):
        """停止GPS"""
        if PLYER_AVAILABLE:
            try:
                from plyer import gps
                gps.stop()
            except:
                pass


class LocationApp(App):
    def build(self):
        self.title = "实时定位 v1.0"
        self.icon = 'icon.png' if platform == 'android' else None
        self.layout = LocationLayout()
        return self.layout
    
    def on_stop(self):
        if hasattr(self, 'layout'):
            self.layout.stop()
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        if hasattr(self, 'layout'):
            Clock.schedule_once(lambda dt: self.layout._init_gps(), 0.5)


if __name__ == '__main__':
    LocationApp().run()
