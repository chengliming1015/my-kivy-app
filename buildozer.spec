name: Build Android APK with Buildozer
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    timeout-minutes: 90  # 延长超时，避免构建中断
    steps:
      - name: 检出代码
        uses: actions/checkout@v4

      - name: 替换阿里云源（加速依赖下载）
        run: |
          sudo sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
          sudo dpkg --add-architecture i386
          sudo apt-get update -y --fix-missing

      - name: 安装完整系统依赖（含32位库）
        run: |
          sudo apt-get install -y --fix-missing \
              git zip unzip openjdk-17-jdk \
              python3-pip autoconf libtool pkg-config \
              zlib1g-dev libncurses5-dev libncursesw5-dev \
              libtinfo5 cmake libffi-dev libssl-dev \
              libsqlite3-dev libbz2-dev libreadline-dev \
              libgdbm-dev liblzma-dev \
              android-sdk-platform-tools android-sdk-build-tools \
              libc6:i386 libncurses5:i386 libstdc++6:i386 libz1:i386

      - name: 设置Python 3.10（兼容buildozer）
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: 安装兼容版Buildozer和Cython
        run: |
          python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
          pip uninstall -y cython buildozer
          pip install buildozer==1.5.0 cython==0.29.36 -i https://pypi.tuna.tsinghua.edu.cn/simple

      - name: 清理旧缓存并构建APK
        run: buildozer android debug --clean

      - name: 上传APK产物
        uses: actions/upload-artifact@v4
        with:
          name: android-apk
          path: ./bin/*.apk
