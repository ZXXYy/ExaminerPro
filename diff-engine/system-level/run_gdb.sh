#!/bin/bash
if [ "$1" != "arm" ] && [ "$1" != "thumb" ] && [ "$1" != "arm64" ]; then
    echo "Mode must be one of: arm, thumb, arm64"
    exit 1
fi

DUMP_SCRIPT="$1"
cur_dir=$(pwd)
vmlinux_path=$cur_dir/../../test-generator/build/vmlinux_$1

gdb-multiarch $vmlinux_path --command="./script_gdb/${DUMP_SCRIPT}_$2.gdb"