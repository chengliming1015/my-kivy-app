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
arch = armeabi-v7a
ndk = 25b
sdk = 24
ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
sdk_path = /home/runner/.buildozer/android/platform/android-sdk
ant_path = /usr/bin/ant
gradle_path = /usr/bin/gradle
python3 = True
requirements = python3,kivy==2.3.0,pillow==10.1.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE
android.api = 33
android.ndk_api = 24
android.sdk_build_tools_version = 33.0.2
android.enable_androidx = True
android.gradle_dependencies = 'com.google.android.material:material:1.5.0'

[ios]
ios.deployment_target = 12.0
