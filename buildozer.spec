[app]
# 基础配置（确保不报错，已解决之前的配置缺失问题）
title = KivyHappyNewYear2026
package.name = kivynewyear
package.domain = org.example
source.dir = .
source.main = main.py
version = 1.0.0

# 安卓配置（修正警告，已解决hostpython3、Build Tools依赖问题）
android.ndk = r25c
android.build_tools = 29.0.3
android.archs = armeabi-v7a  # 修正弃用警告，替代旧的android.arch
android.output_dir = ./bin  # 强制输出到./bin，方便捕获APK
android.sdk = 31

# 日志配置（方便排查，不影响打包）
log_level = 2

[buildozer]
# 核心配置（保留之前验证成功的设置）
log_level = 2
warn_on_root = 1
