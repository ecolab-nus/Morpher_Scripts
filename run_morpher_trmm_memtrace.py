import os
import os.path
from os import O_TRUNC, listdir
from os.path import isfile, join
import re
import numpy as np
from tqdm import tqdm
############################################
# Directory Structure:
# Morpher Home:
#     -Morpher_DFG_Generator
#     -Morpher_CGRA_Mapper
#     -hycube_simulator
#     -Morpher_Scripts

# Build all three tools before running this script

def main():
    if not 'MORPHER_HOME' in os.environ:
        raise Exception('Set MORPHER_HOME directory as an environment variable (Ex: export MORPHER_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)')

    MORPHER_HOME = os.getenv('MORPHER_HOME')
    DFG_GEN_HOME = MORPHER_HOME + '/Morpher_DFG_Generator'
    SIMULATOR_HOME = MORPHER_HOME + '/hycube_simulator'
    DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/trmm/'
    SIMULATOR_KERNEL = SIMULATOR_HOME + '/applications/trmm/'
    DFG_MEMTRACE = DFG_GEN_KERNEL + 'memtraces/'

    files = [f for f in listdir(DFG_MEMTRACE) if isfile(join(DFG_MEMTRACE, f)) and re.match("loop_trmm_INNERMOST_LN111_[0-9]*\.txt", f)]
    print("Number of memtraces to be verified: "+str(len(files)))
    samplefiles = np.random.choice(files, size=10000, replace=False)
    for file in tqdm(samplefiles):
        os.system('cp '+join(DFG_MEMTRACE, file)+' '+SIMULATOR_KERNEL)
        command = SIMULATOR_HOME+'/src/build/hycube_simulator '+SIMULATOR_KERNEL+'*.bin '+join(DFG_MEMTRACE, file)+' '+SIMULATOR_KERNEL+'trmm_INNERMOST_LN111_mem_alloc.txt'
        os.system(command+"|tail -n 2 |head -n 1 > output.log")
        with open("output.log", 'r') as f:
            line = f.readline()
            if not re.search("Mismatches::0", line):
                print("ERROR: FAIL AT MEMTRACE "+ file)
    print("Done!")


if __name__ == '__main__':
  main()
