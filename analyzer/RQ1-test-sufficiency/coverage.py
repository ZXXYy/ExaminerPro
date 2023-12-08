import subprocess
import os

encoding = 'T16'
strategy = 'symbolic'
level = 'user'

if encoding in ['T16', 'T32', 'A32']:
    arch = 'AArch32'
    cpu = 'cortex-a7'
else:
    arch = 'AArch64'
    cpu = 'cortex-a72'

if encoding in ['T16', 'T32']:
    mode = 'thumb'
elif encoding == 'A32':
    mode = 'arm'
elif encoding == 'A64':
    mode = 'arm64'

def get_coverage_info(dir, strategy, level, encoding, flag):
    outfile = f'coverage-{strategy}-{level}-{encoding}-all.info' if flag else f'coverage-{strategy}-{level}-{encoding}.info'
    subprocess.run(['lcov', '--capture', '--directory', dir, '--output-file', outfile], check=True)
    subprocess.run(['lcov', '--remove', outfile, '/usr/*', '-o', outfile], check=True)

def remove_gcda_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.gcda'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Removed: {file_path}")


def test_user_level_coverage():
    user_scripts_to_run = [
        "../../test-generator/pickleInsts.py",
        "../../test-generator/genTests.py",
        '../../diff-engine/user-level/run_qemu.py'
    ]

    if strategy == 'symbolic':
        inputfile = f'../../test-generator/build/{strategy}/{encoding}/{encoding}.txt'
    else:
        inputfile = f'./{strategy}/{encoding}/{encoding}_0.txt'
    temp = inputfile.split('/')[-1]
    user_scripts_arguments = [
        [inputfile, strategy, encoding],
        ['--file', f'pickled_{temp}', 
        '--mode', mode,
        '--level', 'user'
        ],
        [f'testcases-{level}-{mode}/',
        '--env', 'qemu',
        '--cpu', cpu,
        ]
    ]

    try:
        subprocess.run(['python3', user_scripts_to_run[0]] + user_scripts_arguments[0], check=True)
        subprocess.run(['python3', user_scripts_to_run[1]] + user_scripts_arguments[1], check=True)
        subprocess.run(['python3', user_scripts_to_run[2]] + user_scripts_arguments[2], check=True)
        subprocess.run(['rm', f'pickled_{temp}'], check=True)
        subprocess.run(['rm', '-r', f'./testcases-{level}-{mode}/'], check=True)
        subprocess.run(['rm', '-r', f'./state_qemu'], check=True)
        # get coverage info
        get_coverage_info('/home/zxy/qemu/build/libqemu-arm-linux-user.fa.p', strategy, level, encoding, False)
        get_coverage_info('/home/zxy/qemu/build', strategy, level, encoding, True)
        # clear gcda data
        remove_gcda_files('/home/zxy/qemu/build')


    except subprocess.CalledProcessError as e:
        print(f"Error running: {e}")

def test_system_level_coverage():
    pass

test_user_level_coverage()