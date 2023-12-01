import subprocess
import os

encoding = 'A32'
arch = 'AArch32'
strategy = 'random-symbols'
if arch == 'AArch32':
    xml_file = '../../test-generator/mra_tools/v8.6/ISA_AArch32_xml_v86A-2019-12'
else:
    xml_file =  '../../test-generator/mra_tools/v8.6/ISA_A64_xml_v86A-2019-12'

# run the test case generator script
script_to_run = '../../test-generator/genInsts.py'
script_arguments = [
    '--altslicesyntax', 
    '--demangle', 
    '--verbose', 
    '-o', '../../test-generator/mra_tools/arch/arch', 
    xml_file, 
    '--encoding', encoding, 
    '--arch', arch, 
    '--strategy', strategy
]
try:
    if not os.path.exists(f"{strategy}/{encoding}"):
       os.makedirs(f"{strategy}/{encoding}")
    # Run the script using subprocess
    for i in range(10):
        subprocess.run(['python3', script_to_run] + script_arguments, check=True)
        subprocess.run(['mv', f'{encoding}.txt', f'{strategy}/{encoding}/{encoding}_{i}.txt'], check=True)
        subprocess.run(['mv', f'{encoding}_constraints.json', f'{strategy}/{encoding}/{encoding}_constraints_{i}.json'], check=True)

except subprocess.CalledProcessError as e:
    print(f"Error running {script_to_run}: {e}")