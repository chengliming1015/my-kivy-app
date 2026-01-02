[app]
# 应用基本信息（必填，确保 Buildozer 解析正常）
title = KivyTemplate
package.name = kivytemplate
package.domain = org.kivytemplate
version = 1.0.0

# 项目目录与入口配置（核心：指定 main.py 为入口文件）
source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,kv,atlas  # 包含的文件后缀
source.exclude_exts = spec  # 排除的文件后缀
source.exclude_dirs = .git,__pycache__,build,.github,venv  # 排除的目录

# 应用图标（可选：若没有 icon.png，可注释此行，不影响构建）
icon.filename = icon.png

# 构建模式（指定为调试版，与打包命令 `debug` 对应）
build.mode = debug

[buildozer]
# 日志级别（2 为详细日志，方便排查问题）
log_level = 2
# 根目录警告（1 为开启，避免在根目录构建的风险）
warn_on_root = 1

[android]
# 构建架构（支持 armeabi-v7a 和 arm64-v8a，覆盖大多数 Android 设备）
arch = armeabi-v7a,arm64-v8a

# NDK 配置（与 YML 对齐，固定为 25b，路径一致）
ndk = 25b
ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# SDK 配置（与 YML 对齐，路径一致，版本匹配）
sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.api = 33
android.ndk_api = 21
android.sdk_build_tools_version = 33.0.2

# 构建工具配置（系统已安装，直接指定路径）
ant_path = /usr/bin/ant
gradle_path = /usr/bin/gradle

# Python 配置（启用 Python 3，与依赖版本对应）
python3 = True

# 核心依赖（与 YML 对齐，格式正确，无多余空格，逗号分隔）
requirements = python3,kivy==2.3.0,pillow==10.1.0,cython==0.29.36

# 额外 Android 配置（提升应用兼容性，避免运行时报错）
android.enable_androidx = True
android.gradle_dependencies = 'com.google.android.material:material:1.5.0'
orientation = portrait  # 应用方向：竖屏
fullscreen = 0  # 不开启全屏
android.permissions = INTERNET,ACCESS_WIFI_STATE  # 应用权限

[ios]
# iOS 配置（无需修改，不影响 Android 构建，保留基础配置即可）
ios.deployment_target = 12.0
