[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json  # 兼容你的json文件
source.main.py = main.py  # 明确指定主程序，避免识别错误
version = 0.1

# 安卓核心配置（无改动，保持兼容）
android.ndk = 25b
android.sdk = 24
android.api = 21
android.ndk_api = 21
android.release = False
android.permissions = INTERNET
android.accept_sdk_license = True  # 关键：自动接受许可，避免交互卡死

# 仅保留必要依赖（你的main.py只用到kivy）
requirements = python3,kivy==2.3.0

# 其他配置
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
