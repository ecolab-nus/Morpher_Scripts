  #!/usr/bin/env python
import sys
import os
import os.path
import shutil
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
  MAPPER_HOME = MORPHER_HOME + '/Morpher_CGRA_Mapper'
  SIMULATOR_HOME = MORPHER_HOME + '/hycube_simulator'

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/hycube_v3_design_app_test/Microspeech16/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/hycube8x8_full//Microspeech16/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/hycube8x8_full/Microspeech16/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)



#############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  os.system('./run_pass.sh microspeech_conv_layer_hycube 8 8192')
  os.system('dot -Tpdf microspeech_conv_layer_hycube_INNERMOST_LN13_PartPredDFG.dot -o microspeech_conv_layer_hycube_INNERMOST_LN13_PartPredDFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final')
  list = os.listdir(MEM_TRACE)
  num_memory_traces = 1#len(list)

 # os.system('cp memtraces/loop_microspeech_conv_layer_hycube_INNERMOST_LN13_0.txt '+SIMULATOR_KERNEL)
  os.system('cp -r memtraces/ '+SIMULATOR_KERNEL)
  os.system('cp microspeech_conv_layer_hycube_INNERMOST_LN13_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp microspeech_conv_layer_hycube_INNERMOST_LN13_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp microspeech_conv_layer_hycube_INNERMOST_LN13_PartPred_DFG.xml '+ MAPPER_KERNEL)

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system('rm *.bin') 
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem8x8.json microspeech_conv_layer_hycube_INNERMOST_LN13_mem_alloc.txt 8192 8 hycube_original_mem.json')
  print('\nupdate memory allocation done!\n')
  os.system('../../../build/src/cgra_xml_mapper -d microspeech_conv_layer_hycube_INNERMOST_LN13_PartPred_DFG.xml -x 8 -y 8 -j hycube_original_mem.json -i 12 -t HyCUBE_4REG')
  
  os.chdir(SIMULATOR_KERNEL)
  os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp *.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)
  #list = os.listdir('memtraces')
  #num_memory_traces = 1#len(list)
  for invocations in range(0,num_memory_traces) :
    data_file = SIMULATOR_KERNEL + '/memtraces/loop_microspeech_conv_layer_hycube_INNERMOST_LN13_' + str(invocations) + '.txt'
    os.system('python3 ../../scripts/skipdata.py --cubedata '+data_file)
    data_file_new = 'data_modi_' + str(invocations) + '.txt'
    os.system('cp data_modi.txt '+data_file_new)
  
  invocation = num_memory_traces
  
  for i in range(0,invocation) :
    os.system('../../../src/build/hycube_simulator -c *.bin -d data_modi_' + str(i) +'.txt -a microspeech_conv_layer_hycube_INNERMOST_LN13_mem_alloc.txt -m 65536 -x 8 -y 8 -t 2 | tail -n 2 |head -n 1 > output.log')
    with open("output.log", 'r') as f:
      line = f.readline()
      success = False
      while line:
        if re.search("Mismatches::0", line):
          success = True
          line = f.readline()
      if not success:
        print("ERROR: FAIL AT MEMTRACE "+ i)
  print("Done!")
    

def my_mkdir(dir):
    try:
        os.makedirs(dir)  
    except:
        pass

if __name__ == '__main__':
  main()
