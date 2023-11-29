#!/bin/sh
if [ "$1" = "single" ]
then
DUMP_SCRIPT="dump_one"
else
DUMP_SCRIPT="dump"
fi
if [ "$2" = "real" ]
then
DUMP_SCRIPT="${DUMP_SCRIPT}_real"
fi
if [ "$3" = "1" ]
then
DUMP_SCRIPT="${DUMP_SCRIPT}_board1"
elif [ "$3" = "2" ]
then 
DUMP_SCRIPT="${DUMP_SCRIPT}_board2"
elif [ "$3" = "3" ]
then 
DUMP_SCRIPT="${DUMP_SCRIPT}_board3"
fi
gdb-multiarch build/vmlinux --command="./script_gdb/${DUMP_SCRIPT}.gdb"