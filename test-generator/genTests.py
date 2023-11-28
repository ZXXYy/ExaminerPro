import os
import pickle
import argparse
import click
from tqdm import tqdm

from utils.elf import parse_template


def generate(binary: bytes, offset: int, insts: dict, outdir: str):
    for id, (name, inst) in tqdm(insts.items()):
        binary = binary[:offset] + inst + binary[offset + len(inst) :]
        outpath = os.path.join(outdir, str(id))
        with open(os.open(outpath, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
            f.write(binary)

def kgenerate(binary: bytes, offset: int, offset_mem: int, instsfile, outdir: str, mode: str, testnum: int, dump: bool):
    test_insts = []
    dump_insts = []
    ARM_INST_LEN = 4
    if mode=='arm':
        NUM_INST = 17 
    elif mode=='arm64':
        NUM_INST = 0
    insts_num = len(instsfile.readlines())
    instsfile.seek(0)
    print(insts_num)
    for i, inst in enumerate(instsfile):
        if (i!=0 and i%testnum ==0) or i==insts_num-1:
            outbinary = binary[:offset] 
            temp_offset = offset
            for test_inst in test_insts:
                outbinary += binary[temp_offset : temp_offset+ARM_INST_LEN*NUM_INST] +test_inst + binary[temp_offset+ARM_INST_LEN*(NUM_INST+1) : temp_offset + ARM_INST_LEN*(NUM_INST+2)]
                temp_offset = temp_offset + ARM_INST_LEN*(NUM_INST+2)
            if dump:
                outbinary += binary[temp_offset : offset_mem] 
                temp_offset = offset_mem
                for dump_inst in dump_insts:
                    outbinary += dump_inst + binary[temp_offset + len(dump_inst) : temp_offset + len(dump_inst)*2 ]
                    temp_offset = temp_offset + len(dump_inst)*2

                outbinary += binary[temp_offset:]
            else:
                outbinary += binary[temp_offset : ] 

            outpath = os.path.join(outdir, str(ceil(i/testnum))+".ko")
            print(str(ceil(i/testnum))+".ko")

            with open(os.open(outpath, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
                f.write(outbinary)
            os.system('strip --strip-debug '+outpath)
            test_insts = []
            dump_insts = []
        if mode=='arm64':
            inst = inst.split()[2].encode("ascii")
        else:
            inst = inst.split()[1].encode("ascii")
        inst = bin2bytes(inst, mode)
        sg = StoreTestCaseGenerator(mode)
        dump_mem = sg.get_mem_inst(inst)
        test_insts.append(inst)
        dump_insts.append(dump_mem)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=argparse.FileType('rb'), required=True,
                        help='instruction file to be processed')
    parser.add_argument('--mode', choices=["arm", "thumb", "arm64"], required=True,
                        help='instruction mode')
    parser.add_argument('--level', choices=["system", "user"], required=True,
                        help='instruction mode')
    parser.add_argument('--outdir', type=str, default="testcases",
                        help='The name of the output kernel module')
    # Parse the command-line arguments
    args = parser.parse_args()
    instsfile = args.file
    mode = args.mode
    level = args.level
    outdir =f"{args.outdir}-{level}-{mode}"
    return instsfile, mode, level, outdir


def main():
    instsfile, mode, level, outdir = parse_args()

    insts = pickle.load(instsfile)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if level == "user":
        binary, offset = parse_template(mode, "user")
        generate(binary, offset, insts, outdir)
    elif level == "system":
        binary, offset, offset_mem = parse_template(mode, "system")
        kgenerate(binary, offset, insts, outdir)


if __name__ == "__main__":
    main()
