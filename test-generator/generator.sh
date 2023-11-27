#!/bin/bash
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <arch> <encoding> <mode>"
    exit 1
fi
if [ "$1" != "AArch32" ] && [ "$1" != "AArch64" ]; then
    echo "Arch must be one of: AArch32, AArch64"
    exit 1
fi
if [ "$2" != "A32" ] && [ "$2" != "T32" ] && [ "$2" != "T16" ] && [ "$2" != "A64" ]; then
    echo "Encoding must be one of: A32, T32, T16, A64"
    exit 1
fi
if [ "$3" != "arm" ] && [ "$3" != "thumb" ] && [ "$3" != "arm64" ]; then
    echo "Mode must be one of: arm, thumb, arm64"
    exit 1
fi

if [ "$1" == "AArch32" ]; then
    xml_file="mra_tools/v8.6/ISA_AArch32_xml_v86A-2019-12"
elif [ "$1" == "AArch64" ]; then
    xml_file="mra_tools/v8.6/ISA_A64_xml_v86A-2019-12"
fi


echo "[1] Generating Instructions for $1 $2..."
python3 genInsts.py --altslicesyntax --demangle --verbose -o mra_tools/arch/arch $xml_file --encoding $2 --arch $1

echo "[2] Pickling Instructions for $1 $2..."
python3 pickleInsts.py $2.txt

echo "[3] Generating Test Cases from template for $1 $..."
python3 genTests.py pickled_$2.txt --mode $3

echo "[4] Moving outputs to build"
mkdir build/$2
mv $2.txt build/$2/$2.txt
mv pickled_$2.txt build/$2/pickled_$2.txt
cp -r testcases/ build/$2/testcases
rm -r testcases/