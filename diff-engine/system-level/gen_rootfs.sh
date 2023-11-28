#!/bin/sh
cur_dir=$(pwd)
testcase_dir="$cur_dir/../../test-generator/build/testcases"
target_dir="$cur_dir/../build/rootfs"

cp -r "$testcase_dir-system-arm" "$target_dir-arm"
cd "$target_dir-arm"
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../rootfs-arm.cpio.gz
# cp -r "$ROOT/build/testcases/top.sh" "$ROOT/build/rootfs"
# cp -r "$ROOT/build/testcases/normal/testko/." "$ROOT/build/rootfs"
# cp -r "$ROOT/build/testcases/str/." "$ROOT/build/rootfs/str"
