[app]
title = KivyApp
package.name = kivyapp
package.domain = org.kivyapp
source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,kv
version = 1.0.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[android]
android.ndk = 25b
android.api = 34
android.minapi = 21
android.arch = arm64-v8a,armeabi-v7a
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
