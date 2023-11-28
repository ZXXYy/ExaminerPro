KERNEL_DIR=../linux
PWD := $(shell pwd)
CROSS-ARM := arm-linux-gnueabi-
CROSS-ARM64 := aarch64-linux-gnu-
obj-m += ktemplate.o ktemplate_dump.o
KCFLAGS-ARM='-mcpu=cortex-a7 -march=armv7ve -mfloat-abi=hard -mfpu=vfpv4'
KCFLAGS-ARM64='-march=armv8-a+crc -mtune=cortex-a72'
KCFLAGS-THUMB='-mthumb -mcpu=cortex-a7 -march=armv7ve -mfloat-abi=hard -mfpu=vfpv4'

.PHONY: build
build: ktemplate.c ktemplate_dump.c
	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) KCFLAGS=$(KCFLAGS-ARM) -C $(KERNEL_DIR) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod .tmp_versions modules.order Module.symvers .Makefile.swp
	mv ktemplate.ko ktemplate_arm.ko
	mv ktemplate_dump.ko ktemplate_dump_arm.ko

	make ARCH=arm64 CROSS_COMPILE=$(CROSS-ARM64) KCFLAGS=$(KCFLAGS-ARM64) -C $(KERNEL_DIR) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod .tmp_versions modules.order Module.symvers .Makefile.swp
	mv ktemplate.ko ktemplate_arm64.ko
	mv ktemplate_dump.ko ktemplate_dump_arm64.ko

	make ARCH=arm CROSS_COMPILE=$(CROSS-ARM) KCFLAGS=$(KCFLAGS-THUMB) -C $(KERNEL_DIR) M=$(PWD) modules
	rm .*.cmd *.o *.mod.c  *.mod .tmp_versions modules.order Module.symvers .Makefile.swp
	mv ktemplate.ko ktemplate_thumb.ko
	mv ktemplate_dump.ko ktemplate_dump_thumb.ko

ktemplate.c: genTemplate.py template.c
	python3 genTemplate.py --file template.c --outfile ktemplate

ktemplate_dump.c: genTemplate.py template.c
	python3 genTemplate.py --file template.c --outfile ktemplate --dumpflag true

clean:
	rm -f template_arm template_thumb template_arm64 template_arm_dump template_thumb_dump template_arm64_dump ktemplate.c ktemplate_dump.c