import os
import pickle
import argparse
from math import ceil
from tqdm import tqdm

from utils.elf import parse_template
from utils.utils import bin2bytes


def generate(binary: bytes, offset: int, insts: dict, outdir: str):
    for id, (name, inst) in tqdm(insts.items()):
        binary = binary[:offset] + inst + binary[offset + len(inst) :]
        outpath = os.path.join(outdir, str(id))
        with open(os.open(outpath, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
            f.write(binary)

def kgenerate(mode, binary: bytes, offset: int, offset_mem: int, insts: dict, outdir: str, testnum: int, dump: bool):
    test_insts = []
    ARM_INST_LEN = 4
    insts_num = len(insts)
    print(insts_num)
    for i, (name, inst) in tqdm(insts.items()):
        if (i!=0 and i%testnum ==0) or i==insts_num-1:
            outbinary = binary[:offset] 
            temp_offset = offset
            for test_inst in test_insts:
                outbinary += binary[temp_offset : temp_offset] +test_inst + binary[temp_offset+ARM_INST_LEN : temp_offset + ARM_INST_LEN*2]
                temp_offset = temp_offset + ARM_INST_LEN*2
            if dump:
                outbinary += binary[temp_offset : offset_mem] 
                temp_offset = offset_mem
                for dump_inst in test_insts:
                    outbinary += dump_inst + binary[temp_offset + len(dump_inst) : temp_offset + len(dump_inst)*2 ]
                    temp_offset = temp_offset + len(dump_inst)*2
                outbinary += binary[temp_offset:]
            else:
                outbinary += binary[temp_offset : ] 

            outpath = os.path.join(outdir, str(ceil(i/testnum))+".ko")
            print(str(ceil(i/testnum))+".ko")

            with open(os.open(outpath, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
                f.write(outbinary)
            if mode == "arm64":
                os.system(f'aarch64-linux-gnu--strip --strip-debug '+outpath)
            else:
                os.system(f'arm-linux-gnueabi-strip --strip-debug '+outpath)
            
            test_insts = []
        test_insts.append(inst)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=argparse.FileType('rb'), required=True,
                        help='instruction file to be processed')
    parser.add_argument('--mode', choices=["arm", "thumb", "arm64"], required=True,
                        help='instruction mode')
    parser.add_argument('--outdir', type=str, default="testcases",
                        help='The name of the output kernel module')
    parser.add_argument('--level', choices=["system", "user"], required=True,
                        help='instruction mode')
    parser.add_argument('--number', type=int, default=100000,
                        help='The number of testcases to be generated in one kernel module at system level')
    parser.add_argument('--dumpflag', type=bool, default=False,
                        help='If instruction is `str`, dump the memory it writes to at system level')
    # Parse the command-line arguments
    args = parser.parse_args()
    instsfile = args.file
    mode = args.mode
    level = args.level
    outdir =f"{args.outdir}-{level}-{mode}"
    testnum = args.number
    dumpflag = args.dumpflag
    return instsfile, mode, level, outdir, testnum, dumpflag


def main():
    instsfile, mode, level, outdir, testnum, dumpflag = parse_args()
    insts = pickle.load(instsfile)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if level == "user":
        binary, offset, _ = parse_template(mode, "user")
        generate(binary, offset, insts, outdir)
    elif level == "system":
        binary, offset, offset_mem = parse_template(mode, "system")
        kgenerate(mode, binary, offset, offset_mem, insts, outdir, testnum, dumpflag)


if __name__ == "__main__":
    main()
