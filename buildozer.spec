[app]
# ================= 第一部分：应用基本信息 =================
title = 文斌工作室
package.name = chengliming
package.domain = org.test
version = 0.1
android.numeric_version = 1

# 图标和启动图
icon.filename = ./chengliming.png
presplash.filename = ./splashscreen.png
presplash.color = #0A0A1A  

# 应用显示设置
orientation = portrait
fullscreen = 0

# ================= 第二部分：源代码配置 =================
source.dir = .
source.main = main.py  
source.include_exts = py,png,jpg,kv,atlas,ttf,ttc,json,txt 
source.include_patterns = fonts/*

# ================= 第三部分：依赖和SDK配置 =================
requirements = python3, kivy==2.2.1, plyer==2.1.0,,android

# Android SDK配置
android.accept_sdk_license = True
android.api = 33          
android.minapi = 21       
android.sdk = 33          
android.ndk = 25b        
android.archs = arm64-v8a  

# Android功能配置
android.private_storage = True   
android.enable_androidx = True   
android.build_cache = True

# ================= 第四部分：权限配置 =================
# 简化权限：去掉ACCESS_BACKGROUND_LOCATION，除非你真的需要后台定位
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, INTERNET
android.features = android.hardware.location.gps

# ================= 第五部分：输出和日志 =================
android.output_dir = ./bin
log_level = 2  # 

[buildozer]
log_level = 2
workdir = ./.buildozer
