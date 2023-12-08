#!/bin/bash
python3 generator.py --encoding A32 --strategy symbolic
python3 generator.py --encoding A64 --strategy symbolic
python3 generator.py --encoding T32 --strategy symbolic
python3 generator.py --encoding T16 --strategy symbolic

python3 generator.py --encoding A32 --strategy random-symbols
python3 generator.py --encoding A64 --strategy random-symbols
python3 generator.py --encoding T32 --strategy random-symbols
python3 generator.py --encoding T16 --strategy random-symbols
