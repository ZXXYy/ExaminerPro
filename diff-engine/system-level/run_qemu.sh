#!/bin/bash
cur_dir=$(pwd)
image_dir="/home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm64"
qemu-system-aarch64 -M virt \
	-kernel /home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm64 \
	-cpu cortex-a72 \
	-initrd ../build/rootfs-arm64.cpio.gz -append "root=/dev/mem console=ttyAMA0" \
	-s -nographic -m size=1G

# /home/zxy/qemu/build/qemu-system-arm -M raspi2b -cpu cortex-a7 \
# 	-kernel /home/zxy/TSE-ExaminerPro/test-generator/build/zImage_arm \
# 	-dtb ../build/bcm2709-rpi-2-b.dtb \
# 	-initrd ../build/rootfs-arm.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
# 	-s -nographic -m size=1024


# qemu-system-arm -M raspi2b -cpu cortex-a7 \
# 	-kernel build/zImage \
#     -dtb build/bcm2709-rpi-2-b.dtb \
# 	-initrd build/rootfs.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
# 	-s -nographic -m size=1024