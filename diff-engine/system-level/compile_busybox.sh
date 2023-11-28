#!/bin/sh
if [ "$1" = "armv7" ]
then
cd ../armv7/busybox-1.33.1
# make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
# make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- install
cp -av _install/* ../build/rootfs/
elif [ "$1" = "armv8" ]
then
cd ../armv8/busybox-1.33.1
# make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
# make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- install
cp -av _install/* ../build/rootfs/
else
echo "please choose from armv7, armv8"
fi