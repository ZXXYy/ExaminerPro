import os
import time
import subprocess
import multiprocessing
from os import path
from subprocess import TimeoutExpired
from argparse import ArgumentParser
from tqdm import tqdm
import sys
 
directory = path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(directory))
from utils import pickle_file

timeout = set()
lock = multiprocessing.Lock()

def work(cmd, outfile):
    global timeout, lock
    with open(outfile, "w") as f:
        try:
            subprocess.run(
                cmd, stdout=f, stderr=subprocess.PIPE, timeout=5
            )
        except TimeoutExpired:
            with lock:
                timeout.add(int(cmd[-1].split('/')[-1]))

def init_pool_processes(the_lock):
    '''Initialize each process with a global variable lock.
    '''
    global lock
    lock = the_lock

def run(testcases_dir, output_dir, cmd):
    task_cmds = []
    task_outfiles = []
    testcases = os.listdir(testcases_dir)
    for filename in tqdm(testcases):
        testcase_path = path.join(testcases_dir, filename)
        output_path = path.join(output_dir, filename)
        task_cmds.append(cmd + [testcase_path])
        task_outfiles.append(output_path)
    
    count = multiprocessing.cpu_count()
    print(f"cpu cores = {count}")
    pool = multiprocessing.Pool(processes=count, initializer=init_pool_processes, initargs=(lock,))
    pool.starmap(work, tqdm([(item, task_outfiles[i]) for i, item in enumerate(task_cmds)], total=len(task_cmds)))
    

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
        cmds = ["/home/zxy/qemu/build/aarch64-linux-user/qemu-aarch64", "-cpu", cpu]
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
