import argparse
from os import path

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=argparse.FileType('r'), required=True,
                        help='template file to be processed')
    parser.add_argument('--number', type=int, default=100000,
                        help='The number of testcases to be generated in one kernel module')
    parser.add_argument('--dumpflag', type=bool, default=False,
                        help='If instruction is `str`, dump the memory it writes to')
    parser.add_argument('--outfile', type=str, default="ktemplate",
                        help='The name of the output kernel module')
    # Parse the command-line arguments
    args = parser.parse_args()
    tempfile = args.file
    testnum = args.number
    dumpflag = args.dumpflag
    outfile = args.outfile
    return tempfile, testnum, dumpflag, outfile

if __name__ == "__main__":
    tempfile, testnum, dumpflag, outfile = parse_args()
    outfile = outfile+"_dump.c" if dumpflag else outfile+".c"

    lines = []
    templine = "\t\t\t\"{assembly}\\n\"\n"
    for line in tempfile:
        lines.append(line)
        if "inst_location:\\n" in line:
            for i in range(testnum):
                lines.append(templine.format(assembly="nop"))
                if dumpflag:
                    lines.append(templine.format(assembly="b prepare_dump"))
                else:
                    lines.append(templine.format(assembly="b finish_location"))
        if "dump_memory:\\n" in line:
            if dumpflag:
                for i in range(testnum):
                    lines.append(templine.format(assembly="nop"))
                    lines.append(templine.format(assembly="b check_memory"))
            lines.append(templine.format(assembly="nop"))
            lines.append(templine.format(assembly="nop"))
    
    with open (outfile, "w") as f:
        for line in lines:
            f.write(line)   