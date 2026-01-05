from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform
import os

# Android特定导入
if platform == 'android':
    from android.permissions import request_permissions, Permission
    try:
        from plyer import gps
        PLYER_AVAILABLE = True
    except ImportError:
        PLYER_AVAILABLE = False
else:
    PLYER_AVAILABLE = False

class AutoGPSLabel(Label):
    """自动GPS定位标签"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 应用启动时自动请求权限
        Clock.schedule_once(self.request_permissions, 1)
        
        # 设置背景颜色
        Window.clearcolor = (0, 0.1, 0.2, 1)  # 深蓝色背景
        
    def request_permissions(self, dt):
        """请求Android权限"""
        if platform == 'android':
            try:
                required_permissions = [
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                ]
                request_permissions(required_permissions, self.permission_callback)
            except:
                Clock.schedule_once(self.start_gps, 2)
        else:
            self.text = "非Android平台"
    
    def permission_callback(self, permissions, results):
        """权限回调"""
        if all(results):
            Clock.schedule_once(self.start_gps, 1)
        else:
            self.text = "需要位置权限\n请允许位置权限"
            Clock.schedule_once(self.start_gps, 3)  # 3秒后重试
    
    def start_gps(self, dt):
        """启动GPS"""
        if not PLYER_AVAILABLE:
            self.text = "GPS模块不可用"
            return
        
        try:
            # 配置GPS回调
            gps.configure(
                on_location=self.on_location,
                on_status=self.on_status
            )
            # 启动GPS
            gps.start(minTime=3000, minDistance=10)  # 3秒或移动10米更新
            self.text = "正在获取位置..."
        except Exception as e:
            self.text = f"GPS错误:\n{str(e)}"
    
    @mainthread
    def on_location(self, **kwargs):
        """位置更新回调"""
        try:
            lat = kwargs.get('lat', 0)
            lon = kwargs.get('lon', 0)
            accuracy = kwargs.get('accuracy', 0)
            
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                location_text = f"""你的位置：
                
纬度: {lat:.6f}°
经度: {lon:.6f}°
                
精度: {accuracy:.1f}米
                
最后更新: {Clock.get_strftime('%H:%M:%S')}"""
                
                self.text = location_text
                self.color = (0, 1, 0, 1)  # 绿色表示成功
            else:
                self.text = "等待有效位置数据..."
                self.color = (1, 1, 0, 1)  # 黄色表示等待
                
        except Exception as e:
            self.text = f"数据处理错误:\n{str(e)}"
            self.color = (1, 0, 0, 1)  # 红色表示错误
    
    @mainthread
    def on_status(self, stype, status):
        """GPS状态回调（这里我们只处理状态更新，不显示）"""
        pass

class MinimalGPSApp(App):
    """极简GPS应用"""
    # 字体路径
    FONT_PATH = 'fonts/msyhbd.ttc'
    
    def build(self):
        # 设置全屏
        if platform == 'android':
            from android import api_version, mActivity
            Window.fullscreen = 'auto'
        
        # 注册字体
        if os.path.exists(self.FONT_PATH):
            from kivy.core.text import LabelBase
            LabelBase.register(name='YaHeiBold', fn_regular=self.FONT_PATH)
            font_name = 'YaHeiBold'
        else:
            font_name = 'Roboto'
        
        # 创建主标签
        label = AutoGPSLabel(
            font_name=font_name,
            font_size=36,
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, Window.height * 0.9),
            text='启动GPS定位...',
            color=(1, 1, 1, 1)
        )
        
        # 绑定窗口大小变化
        Window.bind(size=self.on_window_size)
        
        return label
    
    def on_window_size(self, instance, size):
        """窗口大小变化时调整文本大小"""
        if self.root:
            self.root.text_size = (size[0] * 0.9, size[1] * 0.9)
    
    def on_stop(self):
        """应用停止时"""
        if platform == 'android' and PLYER_AVAILABLE:
            try:
                gps.stop()
            except:
                pass

if __name__ == '__main__':
    MinimalGPSApp().run()
