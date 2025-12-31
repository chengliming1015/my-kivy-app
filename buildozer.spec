[app]
# 必填：安卓应用包名（符合Java包名规范，小写、点分隔，可自定义）
package.name = com.chengliming.kivappynewyear
# 必填：应用版本号（合法格式即可，如1.0.0、0.1.0）
version = 1.0.0
# 原有配置不变
title = KivyHappyNewYear2026
source.dir = .
source.main.py = main.py
android.ndk = r25c
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25c
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.automatic_ndk = False
android.automatic_sdk = False

[buildozer]
cache_dir = /home/runner/.buildozer/cache
no_cache = True
