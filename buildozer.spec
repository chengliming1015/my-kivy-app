[app]
# 应用信息
title = My Python App
package.name = mypythonapp
package.domain = org.mypython
source.dir = .

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 版本
version = 1.0

# 依赖
requirements = python3,kivy==2.1.0

# 方向
orientation = portrait

# 图标
icon.filename = icon.png

# 权限
android.permissions = INTERNET

# Android 配置
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.accept_sdk_license = True


[buildozer]
log_level = 2
