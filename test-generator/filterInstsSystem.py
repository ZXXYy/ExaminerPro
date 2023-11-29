import click
import logging
import re
import pickle
import os
from tqdm import tqdm
from elftools.elf.elffile import ELFFile
from capstone import (
    Cs,
    CsInsn,
    CsError,
    CS_ARCH_ARM,
    CS_ARCH_ARM64,
    CS_MODE_ARM,
    CS_MODE_THUMB,
)

from keystone import (
    Ks,
    KsError,
    KS_ARCH_ARM,
    KS_ARCH_ARM64,
    KS_MODE_ARM,
    KS_MODE_LITTLE_ENDIAN,
)
from enum import Enum
from utils import *
class InstType(Enum):
    STR = 1
    BR = 2   
    PREVILEGE = 3
    OTHER = 4
    INVALID = 5
class StoreTestCaseGenerator:
    def __init__(self, mode: str):
        self.mode = mode
        self.set_capstone()
        self.set_keystone()

    def set_capstone(self):
        if self.mode == "arm":
            cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        elif self.mode == "thumb":
            cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
        elif self.mode == "arm64":
            cs = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        else:
            raise ValueError("mode is undefined: {}".format(self.mode))
        self.cs = cs

    def set_keystone(self):
        if self.mode in ("arm", "thumb"):
            ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
        elif self.mode == "arm64":
            ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
        else:
            raise ValueError("mode is undefined: {}".format(self.mode))
        self.ks = ks
    
    def get_inst_type(self, inst):
        try:
            cs_insn: CsInsn = next(self.cs.disasm(inst, 0x00), None)
        except CsError as err:
            logging.debug(err)
        if cs_insn:
            inst_name = cs_insn.insn_name()
            op_str = cs_insn.op_str
            # print(inst_name)
            # print(op_str)
            try:
                if self.mode == 'arm64':
                    if inst_name in A64_STR_INSTS:
                        return InstType.STR
                    if inst_name in A64_BR_INSTS:
                        return InstType.BR
                    dst = op_str.split(',')[0]
                    if dst == 'pc' or dst == 'pc!' or dst == 'sp' or dst == 'wsp':
                        # if dst =='wsp':
                        #     print(inst_name)
                        #     print(op_str)
                        return InstType.BR
                    if inst_name in A32_MUL_INSTS:
                        dst = op_str.split(',')[1].strip()
                        if dst == 'pc' or dst == 'pc!' or dst == 'sp' or dst == 'wsp':
                            return InstType.BR
                    if "[" in op_str:
                        position = '[' + op_str.split('[')[1]
                        base_addr = position.split(',')[0][1:]
                        base_addr = base_addr[:-1] if "]" in base_addr else base_addr 
                        if ("!" in position or "], " in position) and (base_addr=='pc' or base_addr=='sp'):
                            return InstType.BR
                    # ld1 {v29.s}[3], [sp], #4
                    m = re.match(r"{.*}.*, \[(.*)\],.*", op_str)
                    if m:
                        if m.group(1) == 'sp':
                            print(inst_name)
                            print(op_str)
                            return InstType.BR
                    return InstType.OTHER
                else:
                    # cpsid, mcr, svc
                    if inst_name in A32_MCR_INSTS:
                        return InstType.PREVILEGE
                    if inst_name in A32_INT_INSTS:
                        return InstType.PREVILEGE
                    if inst_name in ["sha256h2"]:
                        # print(InstType.PREVILEGE)
                        return InstType.PREVILEGE
                    if inst_name in A32_STR_INSTS:
                        position = '[' + op_str.split('[')[1]
                        base_addr = position.split(',')[0][1:]
                        base_addr = base_addr[:-1] if "]" in base_addr else base_addr 
                        if ("!" in position or "], " in position) and (base_addr=='pc' or base_addr=='sp'):
                            return InstType.BR
                        return InstType.STR
                    if inst_name in A32_BR_INSTS:
                        return InstType.BR
                    dst = op_str.split(',')[0]
                    if dst == 'pc' or dst == 'pc!' or dst == 'sp':
                        return InstType.BR
                    if inst_name in A32_MUL_INSTS:
                        dst = op_str.split(',')[1].strip()
                        if dst == 'pc' or dst == 'pc!' or dst == 'sp':
                            return InstType.BR
                    if "[" in op_str:
                        position = '[' + op_str.split('[')[1]
                        base_addr = position.split(',')[0][1:]
                        base_addr = base_addr[:-1] if "]" in base_addr else base_addr 
                        if ("!" in position or "], " in position) and (base_addr=='pc' or base_addr=='sp'):
                            return InstType.BR
                    return InstType.OTHER
            except KsError as err:
                logging.debug("{}: {} {}; {}".format(
                    err, cs_insn.mnemonic, op_str, inserted_inst))
        return InstType.INVALID
    
    def get_dump_inst(self, str_inst):
        if self.mode in ("arm", "thumb"):
            mov_inst = INST_ARM_MOV_R1
        elif self.mode == "arm64":
            mov_inst = INST_ARM64_MOV_R1
        try:
            cs_insn: CsInsn = next(self.cs.disasm(str_inst, 0x00), None)
        except CsError as err:
            logging.debug(err)
        if cs_insn:
            inst_name = cs_insn.insn_name()
            op_str = cs_insn.op_str
            try:
                if self.mode == 'arm64':
                    if inst_name not in A64_STR_INSTS:
                        return mov_inst
                    position = '[' + op_str.split('[')[1]
                    reg_mode = op_str.split(' ')[1][0]
                    if reg_mode in ('w', 'x'):
                        reg = reg_mode + '1'
                    else:
                        return mov_inst
                    inserted_inst = "{} {}, {}".format(inst_name.replace(
                        'st', 'ld'), reg, position.replace('pc', 'x3'))
                    encoding, _ = self.ks.asm(inserted_inst, as_bytes=True)
                    if encoding:
                        return encoding
                    return mov_inst
                else:
                    if inst_name not in A32_STR_INSTS:
                        return mov_inst
                    match = re.search(r"\[.*\]", op_str)
                    position = '[' + op_str.split('[')[1]
                    inserted_inst = "ldr r1," + position.replace('pc', 'r3')
                    # print(inserted_inst)
                    encoding, _ = self.ks.asm(inserted_inst, as_bytes=True)
                    if encoding:
                        return encoding
                    return mov_inst
            except KsError as err:
                logging.debug("{}: {} {}; {}".format(
                    err, cs_insn.mnemonic, op_str, inserted_inst))
        return mov_inst

@click.command()
@click.argument("mode", type=click.Choice(["arm", "thumb", "arm64"]))
@click.argument("instsfile", type=click.File("rb"))
@click.option(
    "--outdir",
    default=".",
    type=click.Path(resolve_path=True),
)
def main(mode, instsfile, outdir):
    if mode=='arm':
        output_suffix = "A32" 
    elif mode=='arm64':
        output_suffix = "A64"
    elif mode=='thumb':
         output_suffix = "T32"
    str_insts = {}
    noraml_insts = {}
    filter_insts = {}

    insts = pickle.load(instsfile)
    for id, (name, inst) in tqdm(insts.items()):
        temp = inst
        if "SHA" in name or "LDRD" in name:
            filter_insts[len(filter_insts)] = (name, inst)
        sg = StoreTestCaseGenerator(mode)
        inst_type = sg.get_inst_type(inst)
        # print(str(id)+" "+str(inst_type))
        if inst_type == InstType.BR or inst_type == InstType.PREVILEGE:
            filter_insts[len(filter_insts)] = (name, inst)
        elif inst_type == InstType.STR:
            str_insts[len(str_insts)] = (name, inst)
        else:
            noraml_insts[len(noraml_insts)] = (name, inst)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open(f'{outdir}/pickled_str_insts_{output_suffix}', 'wb') as f:
        pickle.dump(str_insts, f)
    with open(f'{outdir}/pickled_normal_insts_{output_suffix}', 'wb') as f:
        pickle.dump(noraml_insts, f)
    with open(f'{outdir}/pickled_filter_insts_{output_suffix}', 'wb') as f:
        pickle.dump(filter_insts, f)


if __name__ == "__main__":
    main()
