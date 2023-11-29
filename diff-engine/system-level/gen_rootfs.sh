#!/bin/bash
if [ "$1" != "A32" ] && [ "$1" != "T32" ] && [ "$1" != "T16" ] && [ "$1" != "A64" ]; then
    echo "Encoding must be one of: A32, T32, T16, A64"
    exit 1
fi
if [ "$2" != "random" ] && [ "$2" != "symbolic" ] && [ "$2" != "random-symbols" ]; then
    echo "Mode must be one of: random, random-symbols, symbolic"
    exit 1
fi
if [ "$3" != "arm" ] && [ "$3" != "thumb" ] && [ "$3" != "arm64" ]; then
    echo "Mode must be one of: arm, thumb, arm64"
    exit 1
fi
cur_dir=$(pwd)
testcase_dir="$cur_dir/../../test-generator/build/$2/$1/testcases-system-$3"
target_dir="$cur_dir/../build/rootfs-$3"

cp -r "$testcase_dir" "$target_dir"
cd "$target_dir"
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../rootfs-$3.cpio.gz
# cp -r "$ROOT/build/testcases/top.sh" "$ROOT/build/rootfs"
# cp -r "$ROOT/build/testcases/normal/testko/." "$ROOT/build/rootfs"
# cp -r "$ROOT/build/testcases/str/." "$ROOT/build/rootfs/str"
