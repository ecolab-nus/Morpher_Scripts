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

  DFG_GEN_KERNEL = DFG_GEN_HOME + '/applications/hycube_v3_design_app_test/fft/fft_no_unroll/'
  MAPPER_KERNEL = MAPPER_HOME + '/applications/hycube/fft/'
  SIMULATOR_KERNEL =SIMULATOR_HOME + '/applications/fft/'

  my_mkdir(DFG_GEN_KERNEL)
  my_mkdir(MAPPER_KERNEL)
  my_mkdir(SIMULATOR_KERNEL)



##############################################################################################################################################
  print('\nRunning Morpher_DFG_Generator\n')
  os.chdir(DFG_GEN_KERNEL)

  print('\nGenerating DFG\n')
  os.system('./run_pass.sh fix_fft')
  os.system('dot -Tpdf fix_fft_INNERMOST_LN111_PartPredDFG.dot -o fix_fft_INNERMOST_LN111_PartPredDFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final')
  os.system('cp memtraces/loop_fix_fft_INNERMOST_LN111_0.txt '+SIMULATOR_KERNEL)
  os.system('cp fix_fft_INNERMOST_LN111_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp fix_fft_INNERMOST_LN111_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp fix_fft_INNERMOST_LN111_PartPred_DFG.xml '+ MAPPER_KERNEL)

##############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)


  os.system('rm *.bin')
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original.json fix_fft_INNERMOST_LN111_mem_alloc.txt 2048 2 hycube_original_mem.json')
  print('\nupdate memory allocation done!\n')
  os.system('../../../build/src/cgra_xml_mapper -d fix_fft_INNERMOST_LN111_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem.json -i 21 -t HyCUBE_4REG')

  os.chdir(SIMULATOR_KERNEL)
  os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp *.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)

  os.system('../../src/build/hycube_simulator *.bin loop_fix_fft_INNERMOST_LN111_0.txt fix_fft_INNERMOST_LN111_mem_alloc.txt')

def my_mkdir(dir):
    try:
        os.makedirs(dir)  
    except:
        pass

if __name__ == '__main__':
  main()
