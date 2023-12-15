#!/bin/bash
cur_dir=$(pwd)
if [ "$1" != "arm" ] && [ "$1" != "thumb" ] && [ "$1" != "arm64" ]; then
    echo "Mode must be one of: arm, thumb, arm64"
    exit 1
fi

if [ "$1" == "arm" ]; then
	/home/zxy/qemu/build/qemu-system-arm -M raspi2b -cpu cortex-a7 \
	-kernel /home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm \
	-dtb ../build/bcm2709-rpi-2-b.dtb \
	-initrd ../build/rootfs-arm.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
	-gdb tcp::$2 -nographic -m size=1024
elif [ "$1" == "thumb" ]; then
	/home/zxy/qemu/build/qemu-system-arm -M raspi2b -cpu cortex-a7 \
	-kernel /home/zxy/TSE-ExaminerPro/test-generator/build/zImage_thumb \
	-dtb ../build/bcm2709-rpi-2-b.dtb \
	-initrd ../build/rootfs-thumb.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
	-s -nographic -m size=1024
elif [ "$1" == "arm64" ]; then
	/home/zxy/qemu/build/qemu-system-aarch64 -M virt \
	-kernel /home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm64 \
	-cpu cortex-a72 \
	-initrd ../build/rootfs-arm64.cpio.gz -append "root=/dev/mem console=ttyAMA0" \
	-gdb tcp::$2 -nographic -m size=1G
fi
# image_dir="/home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm64"





# qemu-system-arm -M raspi2b -cpu cortex-a7 \
# 	-kernel build/zImage \
#     -dtb build/bcm2709-rpi-2-b.dtb \
# 	-initrd build/rootfs.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
# 	-s -nographic -m size=1024