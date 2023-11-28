#!/bin/bash
CROSS_ARM=arm-linux-gnueabi-
CROSS_ARM64=aarch64-linux-gnu-
BUSYBOX_DIR_ARM=~/busybox-1.33.1-arm
BUSYBOX_DIR_ARM64=~/busybox-1.33.1-arm64
cur_dir=$(pwd)
rootfs_dst=("$cur_dir/../build/rootfs-arm" "$cur_dir/../build/rootfs-arm64" "$cur_dir/../build/rootfs-thumb")

if [ ! -d "$cur_dir/../build" ]
then
mkdir $cur_dir/../build
fi
for item in "${rootfs_dst[@]}"; do
    if [ ! -d "$item" ]
    then
        mkdir $item
    fi
done


echo "[1] Compiling busybox for arm..."
cd $BUSYBOX_DIR_ARM
# make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig
# make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
make ARCH=arm CROSS_COMPILE=$CROSS_ARM
make ARCH=arm CROSS_COMPILE=$CROSS_ARM install
cp -av _install/* $cur_dir/../build/rootfs-arm/
cd $cur_dir/../build/rootfs-arm
echo "[2] Creating init file for arm..."
touch init
chmod +x init
echo '#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
mknod -m 660 /dev/mem c 1 1
echo -e "\nHello!\n"
exec /bin/sh' > init

echo "[3] Creating standard directory layout for arm..."
mkdir -pv {bin,sbin,etc,proc,sys,usr/{bin,sbin},dev}
cd dev
sudo mknod null c 1 3
sudo mknod console c 5 1
sudo mknod tty2 c 4 2
sudo cp -r $cur_dir/../build/rootfs-arm/* $cur_dir/../build/rootfs-thumb/

# echo "[2] Compiling busybox for arm64..."
# cd $BUSYBOX_DIR_ARM64
# # make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
# # make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
# make ARCH=arm64 CROSS_COMPILE=$CROSS_ARM64
# make ARCH=arm64 CROSS_COMPILE=$CROSS_ARM64 install
# cp -av _install/* $cur_dir/../build/rootfs-arm64/
