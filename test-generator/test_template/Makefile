arm-gcc := arm-linux-gnueabi-gcc
aarch64-gcc := aarch64-linux-gnu-gcc

.PHONY: build
build:
	$(arm-gcc) -static -march=armv7-a -O0 template.c -o template_arm
	$(arm-gcc) -static -mthumb -march=armv7-a -O0 template.c -o template_thumb
	$(aarch64-gcc) -static -march=armv8-a -O0 template.c -o template_arm64

clean:
	rm -f template_arm template_thumb template_arm64