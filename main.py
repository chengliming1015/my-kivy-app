from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform
import os
import time

# Android特定导入
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
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
        self.gps_started = False
        self.last_update_time = 0
        
        # 设置背景颜色
        Window.clearcolor = (0, 0.1, 0.2, 1)
        
        # 应用启动时检查并请求权限
        Clock.schedule_once(self.check_and_request_permissions, 1)
        
    def check_and_request_permissions(self, dt):
        """检查并请求Android权限"""
        if platform == 'android':
            # 首先检查是否已有权限
            has_permission = (
                check_permission(Permission.ACCESS_FINE_LOCATION) or
                check_permission(Permission.ACCESS_COARSE_LOCATION)
            )
            
            if has_permission:
                Clock.schedule_once(self.start_gps, 0.5)
            else:
                # 请求权限
                required_permissions = [
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                ]
                try:
                    request_permissions(required_permissions, self.permission_callback)
                except Exception as e:
                    self.text = f"权限请求失败:\n{str(e)}"
        else:
            self.text = "非Android平台"
            self.start_gps(None)  # 非Android平台模拟
    
    def permission_callback(self, permissions, results):
        """权限回调"""
        if all(results):
            self.text = "权限已授予，正在启动GPS..."
            Clock.schedule_once(self.start_gps, 0.5)
        else:
            # 权限被拒绝，显示提示
            self.text = "位置权限被拒绝\n请到设置中允许位置权限\n然后重启应用"
            self.color = (1, 0.5, 0, 1)  # 橙色提示
    
    def start_gps(self, dt):
        """启动GPS"""
        if not PLYER_AVAILABLE:
            self.text = "GPS模块不可用"
            return
        
        if self.gps_started:
            return  # 避免重复启动
        
        try:
            # 先检查是否有权限（Android）
            if platform == 'android':
                has_perm = (
                    check_permission(Permission.ACCESS_FINE_LOCATION) or
                    check_permission(Permission.ACCESS_COARSE_LOCATION)
                )
                if not has_perm:
                    self.text = "无位置权限\n请允许权限后重启"
                    return
            
            # 配置GPS回调
            gps.configure(
                on_location=self.on_location,
                on_status=self.on_status
            )
            
            # 启动GPS
            gps.start(minTime=5000, minDistance=0)  # 降低要求
            self.gps_started = True
            
            # 设置超时检查
            Clock.schedule_once(self.check_gps_timeout, 30)
            
        except Exception as e:
            self.text = f"GPS启动失败:\n{str(e)}"
            self.color = (1, 0, 0, 1)
    
    def check_gps_timeout(self, dt):
        """检查GPS超时"""
        if "正在获取位置" in self.text or "启动GPS" in self.text:
            self.text = "GPS获取超时\n请确保：\n1. GPS已开启\n2. 在室外空旷区域\n3. 网络可用"
            self.color = (1, 1, 0, 1)
    
    @mainthread
    def on_location(self, **kwargs):
        """位置更新回调"""
        try:
            lat = kwargs.get('lat', 0)
            lon = kwargs.get('lon', 0)
            accuracy = kwargs.get('accuracy', 0)
            speed = kwargs.get('speed', 0)
            
            current_time = time.time()
            
            # 避免更新太频繁
            if current_time - self.last_update_time < 2:
                return
                
            self.last_update_time = current_time
            
            # 验证数据有效性
            if (isinstance(lat, (int, float)) and 
                isinstance(lon, (int, float)) and
                abs(lat) > 0.000001 and 
                abs(lon) > 0.000001):
                
                location_text = f"""位置信息：
                
纬度: {lat:.6f}°
经度: {lon:.6f}°
精度: {accuracy:.1f}米
速度: {speed:.1f} m/s

更新时间: {Clock.get_strftime('%H:%M:%S')}"""
                
                self.text = location_text
                self.color = (0, 1, 0, 1)
            else:
                self.text = "获取位置中...\n(等待有效数据)"
                self.color = (1, 1, 0, 1)
                
        except Exception as e:
            self.text = f"位置处理错误:\n{str(e)}"
            self.color = (1, 0, 0, 1)
    
    @mainthread
    def on_status(self, stype, status):
        """GPS状态回调"""
        status_text = f"GPS状态: {stype} - {status}"
        print(status_text)  # 调试输出
        
        if stype == 'provider-enabled':
            self.text = "GPS已开启，等待定位..."
        elif stype == 'provider-disabled':
            self.text = "GPS已关闭\n请开启定位服务"
            self.color = (1, 0.5, 0, 1)
    
    def cleanup_gps(self):
        """清理GPS资源"""
        if self.gps_started and PLYER_AVAILABLE:
            try:
                gps.stop()
                self.gps_started = False
            except:
                pass

class MinimalGPSApp(App):
    """极简GPS应用"""
    FONT_PATH = 'fonts/simhei.ttf'
    
    def build(self):
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
        self.label = AutoGPSLabel(
            font_name=font_name,
            font_size=32,  # 稍小一点以适应更多信息
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, Window.height * 0.9),
            text='初始化GPS...',
            color=(1, 1, 1, 1)
        )
        
        Window.bind(size=self.on_window_size)
        
        return self.label
    
    def on_window_size(self, instance, size):
        if self.root:
            self.root.text_size = (size[0] * 0.9, size[1] * 0.9)
    
    def on_stop(self):
        """应用停止时清理"""
        if hasattr(self.root, 'cleanup_gps'):
            self.root.cleanup_gps()

if __name__ == '__main__':
    MinimalGPSApp().run()
