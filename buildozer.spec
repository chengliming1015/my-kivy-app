[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.main.py = main.py
source.include_exts = py
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[android]
ndk = 25b
sdk = 24
api = 21
ndk_api = 21
permissions = INTERNET
accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
