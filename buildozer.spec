[app]
title = KivyTemplate
package.name = kivytemplate
package.domain = org.kivytemplate
version = 1.0.0
source.dir = .
# 【新增必填项】指定Python主程序入口（Buildozer解析spec的关键，缺失可能导致依赖传递失败）
source.main.py = main.py
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.exclude_dirs = .git,__pycache__,build,.github
icon.filename = icon.png
# 【新增可选项】指定构建模式为调试版（符合你的打包需求，避免默认模式歧义）
build.mode = debug

[buildozer]
log_level = 2
warn_on_root = 1

[android]
arch = armeabi-v7a,arm64-v8a
ndk = 25b
ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
sdk_path = /home/runner/.buildozer/android/platform/android-sdk
ant_path = /usr/bin/ant
gradle_path = /usr/bin/gradle
python3 = True
# 保留你的核心依赖配置（格式正确，无需修改）
requirements = python3,kivy==2.3.0,pillow==10.1.0,cython==0.29.36
android.api = 33
android.ndk_api = 21
android.sdk_build_tools_version = 33.0.2
android.enable_androidx = True
android.gradle_dependencies = 'com.google.android.material:material:1.5.0'
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE
# 【优化可选项】补充Android包名（与[app]区块保持一致，避免解析歧义）
android.package.name = org.kivytemplate.kivytemplate

[ios]
ios.deployment_target = 12.0
