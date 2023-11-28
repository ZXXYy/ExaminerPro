#!/bin/sh
qemu-system-aarch64 -M virt \
	-kernel build/Image \
	-cpu cortex-a72 \
	-initrd build/rootfs.cpio.gz -append "root=/dev/mem console=ttyAMA0" \
	-s -nographic -m size=1G

qemu-system-arm -M raspi2b -cpu cortex-a7 \
	-kernel build/zImage \
    -dtb build/bcm2709-rpi-2-b.dtb \
	-initrd build/rootfs.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
	-s -nographic -m size=1024

qemu-system-arm -M raspi2b -cpu cortex-a7 \
	-kernel build/zImage \
    -dtb build/bcm2709-rpi-2-b.dtb \
	-initrd build/rootfs.cpio.gz -append "root=/dev/mem/ console=ttyAMA0" \
	-s -nographic -m size=1024