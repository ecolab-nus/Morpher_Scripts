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

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/array_add/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/hycube/array_add/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/array_add/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)



##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  os.system('./run_pass.sh array_add 2 2048')
  os.system('dot -Tpdf array_add_INNERMOST_LN1_PartPredDFG.dot -o array_add_INNERMOST_LN1_PartPredDFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final')
  os.system('cp memtraces/loop_array_add_INNERMOST_LN1_0.txt '+SIMULATOR_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_PartPred_DFG.xml '+ MAPPER_KERNEL)

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system('rm *.bin')  
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem.json array_add_INNERMOST_LN1_mem_alloc.txt 2048 2 hycube_original_mem.json')
  print('\nupdate memory allocation done!\n')
  os.system('../../../build/src/cgra_xml_mapper -d array_add_INNERMOST_LN1_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem.json -t HyCUBE_4REG')

  os.chdir(SIMULATOR_KERNEL)
  os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp *.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)

  os.system('../../src/build/hycube_simulator -c *.bin -d loop_array_add_INNERMOST_LN1_0.txt -a array_add_INNERMOST_LN1_mem_alloc.txt')

def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
  main()
