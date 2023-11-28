#!/bin/sh
if [ "$1" = "armv7" ]
then
ROOT="../armv7"
elif [ "$1" = "armv8" ]
then
ROOT="../armv8"
else
echo "please choose from [armv7, armv8]"
exit 1
fi

cp -r "$ROOT/build/checkcases/." "$ROOT/build/rootfs/check"
cp -r "$ROOT/build/testcases/top.sh" "$ROOT/build/rootfs"
cp -r "$ROOT/build/testcases/normal/testko/." "$ROOT/build/rootfs"
# cp -r "$ROOT/build/testcases/str/." "$ROOT/build/rootfs/str"
cd "$ROOT/build/rootfs"
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../rootfs.cpio.gz