[app]
title = KivyHappyNewYear
package.name = kivynewyear
package.domain = org.example
source.dir = .
source.main = main.py
version = 1.0.0
android.ndk = r25c
android.build_tools = 29.0.3
android.archs = armeabi-v7a  # 修正警告，替换原来的android.arch
android.output_dir = ./bin
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
