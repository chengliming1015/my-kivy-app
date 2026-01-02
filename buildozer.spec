[app]
title = KivyTemplate
package.name = kivytemplate
package.domain = org.kivytemplate
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.exclude_dirs = .git,__pycache__,build,.github
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
[android]
arch = armeabi-v7a,arm64-v8a  # 与命令中的 arch 对应，补充 arm64-v8a
ndk = 25b
ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
sdk_path = /home/runner/.buildozer/android/platform/android-sdk
ant_path = /usr/bin/ant
gradle_path = /usr/bin/gradle
python3 = True
# 核心修复：明确完整依赖，格式正确（无多余空格，逗号分隔），版本对齐
requirements = python3,kivy==2.3.0,pillow==10.1.0,cython==0.29.36
# 核心修复：对齐安装的 platform 33，与日志中的 ANDROIDAPI 统一
android.api = 33
android.ndk_api = 21  # 与命令中的 --ndk-api=21 对应，保持不变
android.sdk_build_tools_version = 33.0.2
android.enable_androidx = True
android.gradle_dependencies = 'com.google.android.material:material:1.5.0'
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE

[ios]
ios.deployment_target = 12.0
