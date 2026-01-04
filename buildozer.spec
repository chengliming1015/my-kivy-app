# This .spec config file tells Buildozer an app's requirements for being built.
# 优化目标：仅生成可用的 Android APK 包（调试版优先，简化冗余配置）

[app]
# 应用核心信息（必填，用于标识 APK 包）
title = My Application
package.name = myapp
package.domain = org.test

# 源码配置（核心，指定入口文件和支持的文件类型）
source.dir = .
source.include_exts = py,png,jpg,kv,atlas  # 仅保留 Kivy 应用必需的文件类型

# 应用版本（用于 APK 包版本标识，无需复杂配置）
version = 0.1

# 核心依赖（仅保留生成 APK 必需的依赖，python3 是基础，kivy 是 UI 框架）
requirements = python3,kivy

# 屏幕方向（固定为竖屏，简化配置，如需横屏可改为 landscape）
orientation = portrait

#
# Android specific（仅保留 APK 打包相关配置，删除无关注释和功能）
#
fullscreen = 0  # 关闭全屏，方便测试操作

# 自动接受 Android SDK 许可（关键：自动化打包无需手动确认，避免卡顿）
android.accept_sdk_license = True

# 目标 Android API 和最低兼容 API（选稳定版本，兼容大多数设备）
android.api = 33
android.minapi = 24

# NDK 版本（指定稳定版本，避免自动下载时版本兼容问题）
android.ndk = 25b

# Android 架构（仅保留 2 种主流架构，减小 APK 体积，适配绝大多数设备）
android.archs = arm64-v8a, armeabi-v7a

# 调试版打包格式（明确指定为 apk，禁用 aab，符合你的需求）
android.debug_artifact = apk

# 发布版打包格式（可选，若后续需要生成发布版 APK，也指定为 apk）
android.release_artifact = apk

# 关闭自动备份（非 APK 核心功能，减少打包冗余）
android.allow_backup = False

# 复制库文件（保持默认，确保 Kivy 依赖正常加载，避免 APK 运行报错）
android.copy_libs = 1

#
# Python for android (p4a) specific（仅保留 APK 打包必需的 p4a 配置）
#
# 指定 p4a 分支（稳定版 master，避免开发版分支的兼容性问题）
p4a.branch = master

# 指定 bootstrap（SDL2 是 Kivy 应用的默认选择，确保 APK 正常运行）
p4a.bootstrap = sdl2

# 忽略 setup.py（简化打包流程，避免不必要的配置解析，适合简单应用）
p4a.setup_py = false

#
# iOS specific（完全删除！因为你仅需要生成 Android APK，iOS 配置无任何意义，减少冗余）
#

[buildozer]
# 日志级别（2 = 调试模式，方便排查 APK 打包问题，后续可改为 1 简化日志）
log_level = 2

# 警告 root 运行（保持开启，避免 root 权限下打包的潜在问题）
warn_on_root = 1

# 打包输出目录（明确指定，方便查找 APK，保持默认即可，无需修改）
build_dir = ./.buildozer
bin_dir = ./bin
