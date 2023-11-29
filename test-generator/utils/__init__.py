__version__ = '0.1.0'

import logging

def configure_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

ERROR_NONE = 0b0
ERROR_PHYSICAL = 0b1
ERROR_EMULATOR = 0b10
ERROR_BOTH = 0b11

MODE = ("arm", "thumb", "arm64")

MEM_SLOT_OFFSET_ARM32 = 44
MEM_SLOT_OFFSET_ARM64 = 64

A32_MCR_INSTS = (
    "mcr",
    "mcr2",
    "mcrr",
    "mcrr2"
)
A32_INT_INSTS = (
    "cps",
    "svc",
    "hvc",
    "hvceq",
    "rfeia"
)
A32_MUL_INSTS = (
    "umull",
    "umlal",
    "smull",
    "smlal",
    "umaal"
)

A32_STR_INSTS = (
    "str",
    "strh",
    "strb",
    "strd",
    "strt",
    "strht",
    "strbt",
    "strex",
    "strexh",
    "strexb",
    "strexd",
    "vstr"
)
A32_BR_INSTS = (
    "b",
    "cbnz",
    "cbz",
    "bl",
    "blx",
    "bx",
    "bxj",
    "tbb",
    "tbh"
)
A64_BR_INSTS = (
    "b",
    "cbnz",
    "cbz",
    "tbz",
    "tbnz",
    "bl",
    "blr",
    "br",
    "ret",
    "blx",
    "bx",
    "bxj",
    "tbb",
    "tbh"
)
A64_STR_INSTS = (
    "str",
    "strb",
    "strh",
    "stur",
    "sturb",
    "sturh",
    "sttr",
    "sttrb",
    "sttrh",
    "stxr",
    "stxrb",
    "stxrh",
    "stlr",
    "stlrb",
    "stlrh",
    "stlur",
    "stlurb",
    "stlurh",
    # "stlxr",
    # "stlxrb",
    # "stlxrh",
    # "stp",
    # "stnp",
    # "stxp",
    # "stlxp",
    "stllrb",
    "stllrh",
    "stllr",
    "st2",
    "st3",
    "st1",
    "st4",
    "stnp",
    "stp",
    "stur"
)

INST_ARM_NOP = b"\x00\xf0\x20\xe3"
INST_ARM_BX_THUMB = b"\x01\x00\x8f\xe2\x10\xff\x2f\xe1"  # add r0, pc, #1; bx r0
INST_THUMB16_NOP = b"\x00\xbf"  # nop
INST_THUMB16_BX_ARM = b"\x78\x47"  # bx pc
INST_THUMB32_MOV_R0_0 = b"\x4f\xf0\x00\x00"  # mov.w r0, #0
INST_ARM_MOV_R1 = b"\x0f\x10\xa0\xe1"  # mov r1, pc  # previous code: mov, r1, #0xbd 
INST_ARM_B_FINISH = b"\xfe\xff\xff\xea"
INST_ARM_B_DUMP = b"\xfe\xff\xff\xea"
INST_ARM64_MOV_R1 = b"\xa1\x17\x80\xd2"  # mov, x1, #0xbd

INST_ARMv5_A32_NOP = b"\x00\x00\xa0\xe1"
INST_ARMv6_A32_NOP = b"\x00\x00\xa0\xe1"
INST_ARMv7_A32_NOP = b"\x00\xf0\x20\xe3"
INST_ARMv7_T32_NOP = b"\x00\xbf"
INST_ARMv8_A64_NOP = b"\x1F\x20\x03\xD5"

INST_ARMv5_A32_MOV_R1_0xBD = b"\xbd\x10\xa0\xe3"
INST_ARMv6_A32_MOV_R1_0xBD = b"\xbd\x10\xa0\xe3"
INST_ARMv7_A32_MOV_R1_0xBD = b"\xbd\x10\xa0\xe3"
INST_ARMv8_A64_MOV_X1_0xBD = b"\xa1\x17\x80\xd2"

INST_ARMv7_A32_BX_THUMB = b"\x01\x00\x8f\xe2" + b"\x10\xff\x2f\xe1"  # add r0, pc, #1; bx r0;
INST_ARMv7_T32_BX_ARM = b"\x78\x47"     # bx pc
INST_ARMv7_T32_MOV_R0_R1 = b"\x08\x46"  # mov r0, r1

# sub r3, pc, #40
INST_ARMv5_A32_SAVE_PC = b"\x28\x30\x4f\xe2" + INST_ARMv5_A32_NOP
INST_ARMv6_A32_SAVE_PC = b"\x28\x30\x4f\xe2" + INST_ARMv6_A32_NOP
INST_ARMv7_A32_SAVE_PC = b"\x28\x30\x4f\xe2" + INST_ARMv7_A32_NOP
# adr x3, .; sub x3, x3, #44
INST_ARMv8_A64_SAVE_PC = b"\x03\x00\x00\x10\x63\xb0\x00\xd1"