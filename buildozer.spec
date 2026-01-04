# 程利明版本的配置文件

[app]
# 安卓安装包的基本信息(必填项)
title = My Application
package.name = myapp
package.domain = org.test

# 源代码路径配置(必填项)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json  # 扩展了常见文件类型

# APP的版本号(必填项)
version = 0.1
android.numeric_version = 1

# 核心依赖（仅保留生成 APK 必需的依赖，python3 是基础，kivy 是 UI 框架）
requirements = python3,kivy

# 自动接受 Android SDK 许可（关键：自动化打包无需手动确认，避免卡顿）
android.accept_sdk_license = True

# 目标 Android API 和最低兼容 API（选稳定版本，兼容大多数设备）
android.api = 33
android.minapi = 28

# NDK 版本（指定稳定版本，避免自动下载时版本兼容问题）
android.ndk = 25b

# CPU架构（建议只使用arm64-v8a，减小体积）
android.archs = arm64-v8a

[buildozer]
# 日志级别（2 = 调试模式，方便排查 APK 打包问题，后续可改为 1 简化日志）
log_level = 2
