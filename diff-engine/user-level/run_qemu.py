import os
import time
import subprocess
from os import path
from subprocess import TimeoutExpired
from argparse import ArgumentParser
from tqdm import tqdm
import sys
 
directory = path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(directory))
from utils import pickle_file

def run(testcases_dir, output_dir, cmds):
    timeout = set()
    for filename in tqdm(os.listdir(testcases_dir)):
        testcase_path = path.join(testcases_dir, filename)
        output_path = path.join(output_dir, filename)
        with open(output_path, "w") as f:
            try:
                subprocess.run(
                    cmds + [testcase_path], stdout=f, stderr=subprocess.PIPE, timeout=5
                )
            except TimeoutExpired:
                timeout.add(int(filename))
    return timeout


ARM_CPU = ["cortex-a7", "arm1176", "arm926", "arm11mpcore"]
AARCH64_CPU = ["cortex-a72"]


def main():
    parser = ArgumentParser()
    parser.add_argument('testcase_dir', type=str)
    parser.add_argument('--env', required=True, type=str, choices=('physical', 'qemu'))
    parser.add_argument('--cpu', type=str, choices=ARM_CPU + AARCH64_CPU)
    args = parser.parse_args()
    env = args.env
    cpu = args.cpu

    state_dir = "state_{}".format(env)
    timeout_file = "timeout_{}".format(env)

    if not path.exists(state_dir):
        os.mkdir(state_dir)

    if env == "physical":
        cmds = []
    elif env == "qemu" and cpu in AARCH64_CPU:
        cmds = ["qemu-aarch64", "-cpu", cpu]
    elif env == "qemu" and cpu in ARM_CPU:
        cmds = ["/home/zxy/qemu/build/arm-linux-user/qemu-arm", "-cpu", cpu]
    else:
        raise ValueError("argument env and cpu is error")

    start_time = time.process_time()

    timeout = run(args.testcase_dir, state_dir, cmds)
    pickle_file(timeout_file, timeout)

    end_time = time.process_time()
    print('time: ', end_time - start_time)


if __name__ == "__main__":
    main()
