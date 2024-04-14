## Examiner-Pro: Testing Arm Emulators across Different Privileges
Emulators are commonly employed to construct dynamic analysis frameworks due to their ability to perform fine-grained tracing, monitor full system functionality, and run on diverse operating systems and architectures. The consistency of emulators with the real devices, remains uncertain. To address this issue, our objective is to automatically identify inconsistent instructions that exhibit different behavior between emulators and real devices across distinct privileges, including user-level and system-level privilege.

We target the Arm architecture, which provides machine-readable specifications. Based on the specification, we propose a sufficient test case generator by designing and implementing the first symbolic execution engine for the Arm architecture specification language (ASL). 

We generated 2,774,649 representative instruction streams and developed a differential testing engine, \ksysname. With this engine, we compared the behavior of real Arm devices across different instruction sets (A32, A64, T16, and T32) with the popular QEMU emulator, both at the user-level and system-level. To demonstrate the generalizability of \ksysname, we also tested two other emulators, namely Unicorn and Angr. We find that undefined implementation in Arm manual and bugs of emulators are the major causes of inconsistencies. 

Furthermore, we discover 17 bugs, which influence commonly used instructions (e.g.,  \code{BLX}). With the inconsistent instructions, we build three security applications and demonstrate the capability of these instructions on detecting emulators, anti-emulation, and anti-fuzzing.

### Reproduce the Results
- Requirements:
```
Python 3.9+
QEMU 7.2.0
gcov 11.4.0
```
If you want to reproduce the results in the real device, than you will need these boards:
- OLinuXino iMX233 for ARMv5
- RaspberryPi Zero for ARMv6
- RaspberryPi 2B for ARMv7
- Hikey 970 for ARMv8

#### Test Case Generation
To generate the test cases, run the following commands:
```
cd analyzer/RQ1-test-sufficiency/
# The option for encoding: A64, A32, T16, T32
# The option for strategy: random, random-symbols, symbolic
python3 generator.py --encoding <your-encoding> --strategy <your-strategy>
```
To get the coverage of test cases after the generation, run the following commands:
```
cd analyzer/RQ1-test-sufficiency/
# you can specify the encodings, strategies, privileges in the coverage.py
python3 coverage.py
```
For further convenience, we published our test cases of three strategies in zip file under /data directory. 

#### Differential Testing Engine
All codes related to differential testing engine is under `/diff-engine`.
- /user-level
    - you could run the `run_qemu.py`, `run_angr.py`, `run_unicorn.py` to collect the results of the execution of the generated test cases.

- /system-level
    1. Run the following commands to get a busybox root filesystem
    ```
    wget http://busybox.net/downloads/busybox-1.24.2.tar.bz2
    tar xf busybox-1.24.2.tar.bz2
    ./compile_busybox.sh
    ```
    2. Use the modified linux image in our /data directory.
    3. Copy the generated test kernel module into the root file system, and run `gen_rootfs.sh` to generate the rootfs-xxx.cpio.gz
    4. `run_qemu.sh <arch>` to start the qemu
    5. `run_gdb.sh <arch> ` to trace the execution results