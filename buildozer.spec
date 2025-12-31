[app]
# 应用名称（不能有空格/特殊字符）
title = MyApp
# 包名（必须是反向域名格式，比如com.你的用户名.应用名）
package.name = myapp
package.domain = org.example
# 主程序文件（你的入口py文件，比如main.py）
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
# 版本号
version = 0.1

# 安卓配置
android.ndk = 25b
android.sdk = 24
# 最低安卓版本
android.api = 21
# 目标安卓版本
android.ndk_api = 21
# 构建模式（debug/ release）
android.release = False
# 权限（根据需要添加，比如INTERNET/ CAMERA等）
android.permissions = INTERNET

# Python依赖（你的项目需要的包，比如kivy/kivymd/requests等）
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

# 其他配置
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0

[buildozer]
# 日志级别
log_level = 2
# 构建失败时保留日志
warn_on_root = 1
