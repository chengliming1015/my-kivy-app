# 程利明版本的配置文件（✅ 标记：修正后的配置）

[app]
# 安卓安装包的基本信息
title = 文斌工作室
package.name = chengliming
package.domain = org.test
icon.filename = ./chengliming.png

# ########### ✅ 修正1：安卓启动页（闪屏页）配置（贴合圣诞树氛围）###########
# 启动页图片路径（需准备 splashscreen.png 放在项目根目录）
presplash.filename = ./splashscreen.png
# 启动页背景色（与圣诞树深夜蓝背景一致）
android.presplash_color = #0A0A1A

# 源代码路径配置
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# APP的版本号
version = 0.1
android.numeric_version = 1

# 核心依赖
requirements = python3,kivy==2.2.1

# 自动接受 Android SDK 许可
android.accept_sdk_license = True

# 目标 Android API 和最低兼容 API
android.api = 33
android.minapi = 28

# CPU架构
android.archs = arm64-v8a

# ########### ✅ 修正3：圣诞树安卓专属适配配置 ###########
# 屏幕方向（landscape：横屏，圣诞树在横屏时展示更完整）
android.orientation = landscape
# 禁用全屏（0=显示手机状态栏/导航栏）
android.fullscreen = 0

# 日志级别（调试时建议设为2）
log_level = 2

[buildozer]
# Buildozer日志级别
log_level = 2
