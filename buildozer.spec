# 程利明版本的配置文件（✅ 标记：修正后的配置 + 补充定位功能必备配置）

[app]
# 安卓安装包的基本信息
# ✅ 注意：title 建议避免纯中文（部分低版本安卓设备可能出现乱码，保留中文同时可补充英文备注）
title = 文斌工作室 (WenBin Studio)
# ✅ 修正：package.name 必须符合 小写字母、数字、下划线 规则，不能包含大写和中文拼音连写无分隔（原chengliming合法，保留并标注规范）
package.name = chengliming
# ✅ 修正：package.domain 遵循 反向域名 规范（原org.test合法，如需正式发布建议改为自有域名如org.wenbin）
package.domain = org.test
# ✅ 补充：增加图标文件存在性校验提示（若文件不存在，Buildozer会使用默认图标）
icon.filename = ./chengliming.png

# ########### ✅ 修正1：安卓启动页（闪屏页）配置（贴合圣诞树氛围）###########
# 启动页图片路径（需准备 splashscreen.png 放在项目根目录，建议尺寸：1080*1920 或 适配横屏的 1920*1080）
presplash.filename = ./splashscreen.png
# 启动页背景色（与圣诞树深夜蓝背景一致，十六进制颜色值格式合法，保留）
android.presplash_color = #0A0A1A
# ✅ 补充：启动页停留时间（可选，默认2秒，贴合氛围设为3秒）
android.presplash_time = 3000

# 源代码路径配置
source.dir = .
# ✅ 补充：扩展支持的文件格式（增加txt，适配可能的配置文件；保留原有格式，确保资源不丢失）
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt

# APP的版本号
version = 0.1
android.numeric_version = 1

# 核心依赖
# ✅ 修正：补充定位功能必备依赖 plyer（之前的定位应用依赖该库，必须添加）
# ✅ 保留：kivy==2.2.1 固定版本，避免自动升级导致兼容性问题
requirements = python3,kivy==2.2.1,plyer

# 自动接受 Android SDK 许可（保留，避免打包过程中手动交互）
android.accept_sdk_license = True

# 目标 Android API 和最低兼容 API（保留，api33 对应 Android 13，minapi28 对应 Android 9，兼容性良好）
android.api = 33
android.minapi = 28

# CPU架构（保留 arm64-v8a，适配主流安卓手机；如需兼容旧设备可补充 armeabi-v7a）
android.archs = arm64-v8a
# ✅ 可选补充：兼容旧设备架构（如需打包给老手机，取消注释下方一行）
# android.archs = arm64-v8a,armeabi-v7a

# ########### ✅ 修正3：圣诞树安卓专属适配配置 ###########
# 屏幕方向（landscape：横屏，圣诞树在横屏时展示更完整，配置合法，保留）
# ✅ 补充：landscape-sensor 支持横屏自动旋转（更友好，如需固定左/右横屏可改为 landscape-left/landscape-right）
android.orientation = landscape
# 禁用全屏（0=显示手机状态栏/导航栏，配置合法，保留；1=隐藏状态栏，2=完全全屏）
android.fullscreen = 0

# ########### ✅ 新增：定位功能必备 Android 权限配置 ###########
# 必须添加位置权限和网络权限，否则无法获取定位信息
android.permissions = ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET

# ########### ✅ 补充：优化打包配置，避免常见报错 ###########
# 指定 NDK 版本（与 api33 兼容，避免打包时自动下载不兼容版本）
android.ndk = 25b
# 启用缓存（加快二次打包速度）
android.build_cache = True
# 忽略不必要的文件（减少打包体积）
source.exclude_exts = pyc,pyo,~,swp
# 排除项目根目录下的无用文件夹（根据实际项目调整）
source.exclude_dirs = venv,.git,.vscode

# 日志级别（调试时建议设为2，发布时可改为0，保留）
log_level = 2

[buildozer]
# Buildozer日志级别（与上方保持一致，方便调试，保留）
log_level = 2
# ✅ 补充：指定 Buildozer 工作目录，避免缓存混乱
workdir = ./.buildozer
# ✅ 补充：指定输出目录，APK 文件统一存放至 bin 目录（默认，明确标注）
android.output_dir = ./bin
