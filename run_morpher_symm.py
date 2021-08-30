#!/usr/bin/env python
import sys
import os
import os.path
import shutil
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

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/kernel_symm/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/hycube/kernel_symm/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/kernel_symm'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)



##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  os.system('./run_pass.sh kernel_symm 2 2048')
  os.system('dot -Tpdf kernel_symm_INNERMOST_LN111_PartPred_DFG.xml -o kernel_symm_INNERMOST_LN111_PartPred_DFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final')

  list = os.listdir(MEM_TRACE)
  num_memory_traces = len(list)
  os.system('cp -r memtraces '+SIMULATOR_KERNEL)
  os.system('cp kernel_symm_INNERMOST_LN111_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp kernel_symm_INNERMOST_LN111_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp kernel_symm_INNERMOST_LN111_PartPred_DFG.xml '+ MAPPER_KERNEL)

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system('rm *.bin') 
  
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem.json kernel_symm_INNERMOST_LN111_mem_alloc.txt 2048 2 hycube_original_mem.json')
  print('\nupdate memory allocation done!\n')
  os.system('../../../build/src/cgra_xml_mapper -d kernel_symm_INNERMOST_LN111_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem.json -i 4 -t HyCUBE_4REG')
  
  os.chdir(SIMULATOR_KERNEL)
  os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp *.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)

  os.system('mv kernel_symm_INNERMOST_LN111_mem_alloc.txt mem_alloc.txt')  
  
  for invocations in range(0,num_memory_traces) :
    data_file = 'memtraces/loop_kernel_symm_INNERMOST_LN111_' + str(invocations) + '.txt'
    os.system('../../src/build/hycube_simulator -c *.bin -d '+data_file+ ' -a mem_alloc.txt')

def my_mkdir(dir):
    try:
        os.makedirs(dir)
    except:
        pass

if __name__ == '__main__':
  main()
