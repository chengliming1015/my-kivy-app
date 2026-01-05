# 程利明版本的配置文件（✅ 标记：新增/优化项，保留原有所有核心信息不变）

[app]
# 安卓安装包的基本信息(必填项)【原有配置，无变动】
title = 文斌工作室
package.name = chengliming
package.domain = org.test
icon.filename = ./chengliming.png

# ########### ✅ 新增1：安卓启动页（闪屏页）配置（贴合圣诞树氛围，打包后生效）###########
# 启动页图片路径（需准备 splashscreen.png 放在项目根目录，建议尺寸 1080x1920，PNG格式）
android.splashscreen = ./splashscreen.png
# 启动页背景色（与圣诞树深夜蓝背景一致，避免切换突兀：#0A0A1A 对应 RGB(0.05,0.05,0.1)）
android.splashscreen.background = #0A0A1A
# 启动页图片缩放模式（fit：自适应屏幕，不拉伸变形，保留完整启动页内容）
android.splashscreen.mode = fit
# 启动页显示延迟（3000毫秒=3秒，足够用户看到启动标识，后自动进入圣诞树界面）
android.splashscreen.delay = 3000

# 源代码路径配置(必填项)【原有配置，基础无变动】
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json  # 扩展了常见文件类型
# ✅ 新增2：强制包含圣诞树核心脚本（避免Buildozer打包时遗漏，确保效果正常）
source.include_files = ./kivy_christmas_tree.py

# APP的版本号(必填项)【原有配置，无变动】
version = 0.1
android.numeric_version = 1

# 核心依赖（仅保留生成 APK 必需的依赖，python3 是基础，kivy 是 UI 框架）
# ✅ 优化：指定Kivy稳定版本（适配圣诞树，避免最新版兼容问题，打包更稳定）
# 原有配置：requirements = python3,kivy
requirements = python3,kivy==2.2.1

# 自动接受 Android SDK 许可（关键：自动化打包无需手动确认，避免卡顿）【原有配置，无变动】
android.accept_sdk_license = True

# 目标 Android API 和最低兼容 API（选稳定版本，兼容大多数设备）【原有配置，无变动】
android.api = 33
android.minapi = 28

# CPU架构（建议只使用arm64-v8a，减小体积）【原有配置，无变动】
android.archs = arm64-v8a

# ########### ✅ 新增3：圣诞树安卓专属适配配置（确保显示效果完整、运行流畅）###########
# 屏幕方向（landscape：横屏，圣诞树在横屏时展示更完整，贴合视觉效果；portrait：竖屏）
android.orientation = landscape
# 禁用全屏（0=显示手机状态栏/导航栏，方便用户操作；1=全屏，隐藏状态栏）
android.fullscreen = 0
# 打包Kivy核心资源（确保圣诞树的Canvas绘图、颜色渲染正常，避免闪退/效果缺失）
android.add_assets = kivy/data
android.add_resources = kivy/fonts,kivy/images

[buildozer]
# 日志级别（2 = 调试模式，方便排查 APK 打包问题，后续可改为 1 简化日志）【原有配置，无变动】
log_level = 2
