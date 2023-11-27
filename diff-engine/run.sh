#!/bin/bash
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <env> <mode> <cpu> <encoding>"
    exit 1
fi
if [ "$1" != "physical" ] && [ "$1" != "qemu" ] && [ "$1" != "angr" ] && [ "$1" != "unicorn" ]; then
    echo "Env must be one of: physical, qemu, angr, unicorn"
    exit 1
fi
if [ "$2" != "user" ] && [ "$2" != "system" ]; then
    echo "Mode must be one of: user, system"
    exit 1
fi
if [ "$3" != "cortex-a7" ] && [ "$3" != "arm1176" ] && [ "$3" != "arm926" ] && [ "$3" != "arm11mpcore" ] && [ "$3" != "cortex-a72" ]; then
    echo "CPU must be one of: cortex-a7, arm1176, arm926, arm11mpcore, cortex-a72"
    exit 1
fi
if [ "$4" != "A32" ] && [ "$4" != "T32" ] && [ "$4" != "T16" ] && [ "$4" != "A64" ]; then
    echo "Encoding must be one of: A32, T32, T16, A64"
    exit 1
fi

echo "[1] Testing Instructions in $1 $2-level for $3-$4..."
python3 $2-level/run_$1.py ../test-generator/build/$4/testcases --env $1 --cpu $3

echo "[2] Moving outputs to build"
mkdir build/$3-$4
cp -r state_$1/ build/$3-$4/state_$1
rm -r state_$1/ 