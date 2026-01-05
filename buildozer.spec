[app]
# 应用基本信息
title = 文斌工作室
package.name = chengliming
package.domain = org.test
version = 0.1
android.numeric_version = 1

# 图标和启动页
icon.filename = ./chengliming.png
presplash.filename = ./splashscreen.png
android.presplash_color = #0A0A1A

# 源代码配置
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt
source.exclude_exts = pyc,pyo,~,swp
source.exclude_dirs = venv,.git,.vscode,__pycache__,bin

# 依赖项
requirements = python3,kivy==2.2.1,plyer==2.1.0

# Android 配置
android.accept_sdk_license = True
android.api = 33
android.minapi = 28
android.archs = arm64-v8a

# 屏幕方向  选项：portrait（竖屏）, landscape（横屏）, portrait,sensor, landscape,sensor
android.orientation = portrait

# 全屏模式 0=显示状态栏, 1=隐藏状态栏, 2=完全全屏
android.fullscreen = 0

# 完整的权限配置（包含后台定位权限）
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET,ACCESS_BACKGROUND_LOCATION

# 打包配置
android.ndk = 25b
android.build_cache = True
log_level = 2

# 输出目录
android.output_dir = ./bin

[buildozer]
log_level = 2
workdir = ./.buildozer
