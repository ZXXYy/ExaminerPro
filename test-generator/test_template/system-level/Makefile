KERNEL-DIR-ARM := ~/linux-arm
KERNEL-DIR-ARM64 := ~/linux-arm64
PWD := $(shell pwd)
CROSS-ARM := arm-linux-gnueabi-
CROSS-ARM64 := aarch64-linux-gnu-
obj-m += ktemplate.o ktemplate_dump.o
KCFLAGS-ARM := '-march=armv7ve -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=vfpv4'
KCFLAGS-ARM64 := '-march=armv8-a+crc -mtune=cortex-a72'
KCFLAGS-THUMB := '-mthumb -mcpu=cortex-a7 -march=armv7ve -mfloat-abi=hard -mfpu=vfpv4'

.PHONY: build
build: ktemplate.c ktemplate_dump.c
	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) KCFLAGS=$(KCFLAGS-ARM) -C $(KERNEL-DIR-ARM) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod modules.order Module.symvers
	mv ktemplate.ko ktemplate_arm.ko
	mv ktemplate_dump.ko ktemplate_dump_arm.ko

	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) KCFLAGS=$(KCFLAGS-THUMB) -C $(KERNEL-DIR-ARM) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod modules.order Module.symvers
	mv ktemplate.ko ktemplate_thumb.ko
	mv ktemplate_dump.ko ktemplate_dump_thumb.ko

	make ARCH=arm64 CROSS_COMPILE=$(CROSS-ARM64) KCFLAGS=$(KCFLAGS-ARM64) -C $(KERNEL-DIR-ARM64) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod modules.order Module.symvers
	mv ktemplate.ko ktemplate_arm64.ko
	mv ktemplate_dump.ko ktemplate_dump_arm64.ko


ktemplate.c: genTemplate.py template.c
	python3 genTemplate.py --file template.c --outfile ktemplate

ktemplate_dump.c: genTemplate.py template.c
	python3 genTemplate.py --file template.c --outfile ktemplate --dumpflag true

linux-arm: 
	cd $(KERNEL-DIR-ARM) && \
	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) bcm2709_defconfig && \
	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) KCFLAGS=$(KCFLAGS-ARM)
	cp $(KERNEL-DIR-ARM)/arch/arm/boot/zImage $(PWD)/../../build/zImage_arm
	cp $(KERNEL-DIR-ARM)/vmlinux  $(PWD)/../../build/vmlinux_arm


linux-arm64: 
	cd $(KERNEL-DIR-ARM64) && \
	make ARCH=arm64 CROSS_COMPILE=$(CROSS-ARM64) bcm2711_defconfig && \
	make ARCH=arm64 CROSS_COMPILE=$(CROSS-ARM64) KCFLAGS=$(KCFLAGS-ARM64)
	cp $(KERNEL-DIR-ARM64)/arch/arm64/boot/Image $(PWD)/../../build/zImage_arm64
	cp $(KERNEL-DIR-ARM64)/vmlinux  $(PWD)/../../build/vmlinux_arm64

clean:
	rm -f template_arm template_thumb template_arm64 template_arm_dump template_thumb_dump template_arm64_dump ktemplate.c ktemplate_dump.c