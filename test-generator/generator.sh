#!/bin/bash
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <arch> <encoding> <mode> <strategy>"
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
if [ "$4" != "random" ] && [ "$4" != "symbolic" ] && [ "$4" != "random-symbols" ]; then
    echo "Mode must be one of: random, random-symbols, symbolic"
    exit 1
fi

if [ "$1" == "AArch32" ]; then
    xml_file="mra_tools/v8.6/ISA_AArch32_xml_v86A-2019-12"
elif [ "$1" == "AArch64" ]; then
    xml_file="mra_tools/v8.6/ISA_A64_xml_v86A-2019-12"
fi

if [ "$4" == "random" ]; then
    pickle_file=$2_rand_valid.txt 
else
    pickle_file=$2.txt
fi

# echo "[1] Generating Instructions for $1 $2..."
# python3 genInsts.py --altslicesyntax --demangle --verbose -o mra_tools/arch/arch $xml_file --encoding $2 --arch $1 --strategy $4
cp /home/zxy/TSE-ExaminerPro/test-generator/build/$4/$2/$2.txt $pickle_file
echo "[2] Pickling Instructions for $1 $2..."
python3 pickleInsts.py $pickle_file $4 $2

echo "[3.1] Generating Test Cases from template for $1 $2 at user level..."
python3 genTests.py --file pickled_$pickle_file --mode $3 --level user

# echo "[3.2] Generating Test Cases from template for $1 $2 at system level..."
# echo "[3.2.1] Spliting Test Cases for $1 $2 at system level..."
# python3 filterInstsSystem.py $3 pickled_$pickle_file
# echo "[3.2.2] Generating Test Cases from template..."
# python3 genTests.py --file pickled_normal_insts_$2 --mode $3 --level system
# echo "[3.2.2] Generating str Test Cases from template..."
# python3 genTests.py --file pickled_str_insts_$2 --mode $3 --level system --dumpflag true

# echo "[4] Moving outputs to build"
# if [ ! -d "build/$4" ]; then
#     mkdir "build/$4"
# fi
# if [ ! -d "build/$4/$2" ]; then
#     mkdir "build/$4/$2"
# fi

# mv $2* build/$4/$2/
# mv pickled_$pickle_file build/$4/$2/pickled_$2.txt
# mv pickled_normal_insts_$2 build/$4/$2/pickled_normal_insts_$2
# mv pickled_str_insts_$2 build/$4/$2/pickled_str_insts_$2
# mv pickled_filter_insts_$2 build/$4/$2/pickled_filter_insts_$2

# if [ "$4" == "random" ]; then
#     mv $pickle_file build/$4/$2/$pickle_file
#     mv $2_rand_valid_constraint.json build/$4/$2/$2_rand_valid_constraint.json
# fi

# cp -r testcases-user-$3/  build/$4/$2/testcases-user-$3
# cp -r testcases-system-$3/ build/$4/$2/
# cp -r testcases-system-$3-str/ build/$4/$2/
# rm -r testcases-system-$3/ testcases-system-$3-str/ testcases-user-$3/

# # ./generator.sh  AArch32 A32 arm symbolic
# # ./generator.sh AArch64 A64 arm64 symbolic