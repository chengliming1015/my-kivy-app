[app]
# 项目名称（可自定义，和你的APK名称一致）
title = KivyHappyNewYear2026
# Python主文件（若你的项目主文件不是main.py，修改为你的实际文件名）
source.dir = .
source.main.py = main.py
# 安卓打包配置
android.ndk = r25c
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25c
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
# 禁用自动下载NDK/SDK
android.automatic_ndk = False
android.automatic_sdk = False

[buildozer]
# 禁用缓存，强制使用自定义NDK
cache_dir = /home/runner/.buildozer/cache
no_cache = True
