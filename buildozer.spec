[app]
# 应用名称（手机上显示的APP名称）
title = 2026Firework
# 应用包名（唯一标识，符合Android规范）
package.name = firework2026
# 应用域名（自定义，无需修改）
package.domain = org.yourapp
# 源代码目录（当前根目录，无需修改）
source.dir = .
# 包含的文件后缀（仅打包必要文件，减小APK体积）
source.include_exts = py,png,jpg,kv,atlas
# 额外包含的文件（无额外文件，留空即可）
source.include_files = 
# Android API版本（适配安卓10-14，兼容性最优）
android.api = 33
# Android NDK版本（与Kivy 2.3.0兼容）
android.ndk = 25b
# Android SDK版本（打包工具依赖）
android.sdk = 24
# 项目依赖（Python3 + Kivy 2.3.0，自动下载安装）
requirements = python3,kivy>=2.3.0
# Android权限（图形渲染、网络（可选），保证APP正常运行）
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE
# 应用图标（可自定义，留空使用Kivy默认图标，不影响运行）
android.icon = %(source.dir)s/icon.png
# 依赖库目录（无需额外库，留空即可）
android.libs = libs
# 安卓架构（arm64-v8a，适配绝大多数现代手机）
android.arch = arm64-v8a
# 本地自定义配方（无，留空即可）
p4a.local_recipes = 
# 引导程序（sdl2，Kivy安卓打包标准配置）
p4a.bootstrap = sdl2
# setup.py路径（无，留空即可）
p4a.setup_py = 
version = 1.0.0
android.p4a_version = "2023.07.03"
[buildozer]
# Buildozer命令（Python3运行，适配Ubuntu 22.04环境）
buildozer.cmd = python -m buildozer
# 日志级别（2级，足够排查问题，不冗余）
buildozer.log_level = 2
# 缓存目录（仅在GitHub服务器临时存在，构建后自动销毁）
buildozer.cache_dir = .buildozer
# 配置文件路径（当前文件，无需修改）
buildozer.config_file = buildozer.spec
# 安卓构建目录（临时文件，无需关心）
android.build_dir = ./build
# 安卓APK输出目录（GitHub会自动提取该目录下的APK）
android.dist_dir = ./bin
# 安卓资源目录（无额外资源，留空即可）
android.add_android_assets = assets
android.build_tools = "33.0.0"
