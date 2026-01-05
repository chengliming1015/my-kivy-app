from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader
from android.permissions import request_permissions, Permission, check_permission
from plyer import gps
import os
import time
import glob

class AutoGPSLabel(BoxLayout):
    """Android GPS定位标签，带音乐播放功能"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gps_started = False
        self.last_update_time = 0
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [10, 10, 10, 10]
        
        # 音乐播放相关
        self.music_playing = False
        self.current_song_index = 0
        self.song_list = []
        self.current_sound = None
        self.music_dir = 'music'  # GitHub根目录下的music文件夹
        
        # 设置背景颜色
        Window.clearcolor = (0, 0.1, 0.2, 1)
        
        # 创建主标签 - 显示GPS信息
        self.label = Label(
            font_name='Roboto',
            font_size=28,
            halign='center',
            valign='middle',
            text='初始化GPS...',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.7)
        )
        self.label.bind(size=self.label.setter('text_size'))
        
        # 创建音乐状态标签
        self.music_label = Label(
            font_name='Roboto',
            font_size=20,
            halign='center',
            valign='middle',
            text='音乐: 未加载',
            color=(1, 1, 0.8, 1),
            size_hint=(1, 0.1)
        )
        self.music_label.bind(size=self.music_label.setter('text_size'))
        
        # 创建按钮容器
        self.button_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            spacing=10
        )
        
        # 创建音乐控制按钮
        self.music_btn = ToggleButton(
            text='🎵 播放',
            background_color=(0.2, 0.5, 0.8, 1),
            on_press=self.toggle_music
        )
        
        # 创建下一首按钮
        self.next_btn = ToggleButton(
            text='⏭️ 下一首',
            background_color=(0.3, 0.4, 0.8, 1),
            on_press=self.play_next_song
        )
        
        # 添加按钮到按钮容器
        self.button_box.add_widget(self.music_btn)
        self.button_box.add_widget(self.next_btn)
        
        # 添加到主布局
        self.add_widget(self.label)
        self.add_widget(self.music_label)
        self.add_widget(self.button_box)
        
        # 设置全屏
        Window.fullscreen = 'auto'
        
        # 扫描音乐文件
        Clock.schedule_once(self.scan_music_files, 0.5)
        
        # 应用启动时检查并请求权限
        Clock.schedule_once(self.check_and_request_permissions, 1)
        
    def scan_music_files(self, dt):
        """扫描music目录下的M4A文件"""
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建music目录路径 - 假设music文件夹在GitHub根目录
        # 在GitHub仓库中，music文件夹应该和main.py在同一级目录
        music_path = os.path.join(script_dir, self.music_dir)
        
        print(f"扫描音乐目录: {music_path}")
        
        # 检查music目录是否存在
        if not os.path.exists(music_path):
            print(f"music目录不存在: {music_path}")
            self.music_label.text = "音乐: 目录不存在\n请创建music文件夹"
            return
        
        # 扫描M4A文件
        m4a_files = []
        
        # 查找所有.m4a文件
        for pattern in ['*.m4a', '*.M4A']:
            m4a_pattern = os.path.join(music_path, pattern)
            found_files = glob.glob(m4a_pattern)
            m4a_files.extend(found_files)
        
        if not m4a_files:
            print(f"没有找到M4A文件")
            self.music_label.text = "音乐: 未找到M4A文件\n请将M4A文件放入music目录"
            
            # 列出目录内容用于调试
            try:
                dir_contents = os.listdir(music_path)
                print(f"music目录内容: {dir_contents}")
            except Exception as e:
                print(f"无法列出目录内容: {e}")
        else:
            self.song_list = sorted(m4a_files)
            print(f"找到 {len(self.song_list)} 首M4A歌曲:")
            for song in self.song_list:
                song_name = os.path.basename(song)
                print(f"  - {song_name}")
            
            # 更新音乐标签
            first_song = os.path.basename(self.song_list[0])
            self.music_label.text = f"音乐: 找到 {len(self.song_list)} 首歌曲\n第一首: {first_song}"
            
            # 如果找到歌曲，启用按钮
            if self.song_list:
                self.music_btn.disabled = False
                self.next_btn.disabled = False
            else:
                self.music_btn.disabled = True
                self.next_btn.disabled = True
    
    def toggle_music(self, instance):
        """切换音乐播放状态"""
        if not self.song_list:
            self.music_label.text = "音乐: 没有可播放的文件"
            self.music_btn.state = 'normal'
            return
        
        if self.music_playing:
            self.pause_music()
        else:
            self.play_music()
    
    def play_music(self):
        """播放音乐"""
        if not self.song_list:
            return
        
        try:
            # 停止当前歌曲（如果有）
            if self.current_sound:
                self.current_sound.stop()
                self.current_sound.unload()
                self.current_sound = None
            
            # 加载当前歌曲
            song_path = self.song_list[self.current_song_index]
            song_name = os.path.basename(song_path)
            
            print(f"加载歌曲: {song_name}")
            self.current_sound = SoundLoader.load(song_path)
            
            if self.current_sound:
                self.current_sound.bind(on_stop=self.on_song_finished)
                self.current_sound.volume = 0.7  # 设置音量
                self.current_sound.play()
                self.music_playing = True
                self.music_btn.text = '⏸️ 暂停'
                
                # 更新音乐标签
                self.music_label.text = f"音乐: 正在播放\n{song_name}"
                print(f"开始播放: {song_name}")
            else:
                print(f"无法加载歌曲: {song_path}")
                self.music_label.text = f"音乐: 无法加载\n{song_name}"
                self.current_sound = None
                
        except Exception as e:
            print(f"播放音乐出错: {e}")
            self.music_label.text = f"音乐: 播放失败\n{str(e)[:20]}..."
    
    def pause_music(self):
        """暂停音乐"""
        if self.current_sound and self.current_sound.state == 'play':
            self.current_sound.stop()
            self.music_playing = False
            self.music_btn.text = '🎵 播放'
            
            # 更新音乐标签
            song_name = os.path.basename(self.song_list[self.current_song_index])
            self.music_label.text = f"音乐: 已暂停\n{song_name}"
            print("音乐已暂停")
    
    def play_next_song(self, instance):
        """播放下一首歌曲"""
        if not self.song_list:
            return
        
        # 停止当前歌曲
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound.unload()
            self.current_sound = None
        
        # 切换到下一首
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        
        # 更新显示
        song_name = os.path.basename(self.song_list[self.current_song_index])
        
        # 如果正在播放，立即播放下一首
        if self.music_playing:
            self.play_music()
        else:
            # 只更新显示
            self.music_label.text = f"音乐: 准备播放\n{song_name}"
            print(f"切换到下一首: {song_name}")
    
    def on_song_finished(self, sound):
        """歌曲播放完成回调"""
        print("歌曲播放完成")
        if self.music_playing and len(self.song_list) > 1:
            Clock.schedule_once(lambda dt: self.play_next_song(None), 0.5)
    
    def check_and_request_permissions(self, dt):
        """检查并请求Android权限"""
        # 检查是否已有权限
        has_permission = (
            check_permission(Permission.ACCESS_FINE_LOCATION) or
            check_permission(Permission.ACCESS_COARSE_LOCATION)
        )
        
        if has_permission:
            self.label.text = "权限已授予，正在启动GPS..."
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
                self.label.text = f"权限请求失败:\n{str(e)}"
    
    def permission_callback(self, permissions, results):
        """权限回调"""
        if all(results):
            self.label.text = "权限已授予，正在启动GPS..."
            Clock.schedule_once(self.start_gps, 0.5)
        else:
            # 权限被拒绝，显示提示
            self.label.text = "位置权限被拒绝\n请到设置中允许位置权限\n然后重启应用"
            self.label.color = (1, 0.5, 0, 1)  # 橙色提示
    
    def start_gps(self, dt):
        """启动GPS"""
        if self.gps_started:
            return  # 避免重复启动
        
        try:
            # 先检查是否有权限
            has_perm = (
                check_permission(Permission.ACCESS_FINE_LOCATION) or
                check_permission(Permission.ACCESS_COARSE_LOCATION)
            )
            if not has_perm:
                self.label.text = "无位置权限\n请允许权限后重启"
                return
            
            # 配置GPS回调
            gps.configure(
                on_location=self.on_location,
                on_status=self.on_status
            )
            
            # 启动GPS
            gps.start(minTime=5000, minDistance=0)
            self.gps_started = True
            
            # 设置超时检查
            Clock.schedule_once(self.check_gps_timeout, 30)
            
        except Exception as e:
            self.label.text = f"GPS启动失败:\n{str(e)}"
            self.label.color = (1, 0, 0, 1)
    
    def check_gps_timeout(self, dt):
        """检查GPS超时"""
        if "正在获取位置" in self.label.text or "启动GPS" in self.label.text:
            self.label.text = "GPS获取超时\n请确保：\n1. GPS已开启\n2. 在室外空旷区域\n3. 网络可用"
            self.label.color = (1, 1, 0, 1)
    
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
                
                self.label.text = location_text
                self.label.color = (0, 1, 0, 1)
            else:
                self.label.text = "获取位置中...\n(等待有效数据)"
                self.label.color = (1, 1, 0, 1)
                
        except Exception as e:
            self.label.text = f"位置处理错误:\n{str(e)}"
            self.label.color = (1, 0, 0, 1)
    
    @mainthread
    def on_status(self, stype, status):
        """GPS状态回调"""
        status_text = f"GPS状态: {stype} - {status}"
        print(status_text)  # 调试输出
        
        if stype == 'provider-enabled':
            self.label.text = "GPS已开启，等待定位..."
        elif stype == 'provider-disabled':
            self.label.text = "GPS已关闭\n请开启定位服务"
            self.label.color = (1, 0.5, 0, 1)
    
    def cleanup_gps(self):
        """清理GPS资源"""
        if self.gps_started:
            try:
                gps.stop()
                self.gps_started = False
            except:
                pass
        
        # 停止音乐播放
        if self.current_sound:
            try:
                self.current_sound.stop()
                self.current_sound.unload()
                self.current_sound = None
            except:
                pass

class MinimalGPSApp(App):
    """极简GPS应用"""
    
    def build(self):
        # 设置全屏
        Window.fullscreen = 'auto'
        
        # 创建主布局
        self.label = AutoGPSLabel()
        
        Window.bind(size=self.on_window_size)
        
        return self.label
    
    def on_window_size(self, instance, size):
        if self.root:
            # 保持布局自适应
            pass
    
    def on_stop(self):
        """应用停止时清理"""
        if hasattr(self.root, 'cleanup_gps'):
            self.root.cleanup_gps()

if __name__ == '__main__':
    MinimalGPSApp().run()
