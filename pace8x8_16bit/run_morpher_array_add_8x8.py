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
  os.system('./run_pass.sh array_add > dfg.log')
  os.system('dot -Tpdf array_add_INNERMOST_LN1_PartPredDFG.dot -o array_add_INNERMOST_LN1_PartPredDFG.pdf')

  MEM_TRACE = DFG_GEN_KERNEL + '/memtraces'

  my_mkdir(MEM_TRACE)

  print('\nGenerating Data Memory Content\n')
  os.system('./final > mem.log')
  list = os.listdir(MEM_TRACE)
  num_memory_traces = len(list)
 # print len([name for name in os.listdir('.') if os.path.isfile(name)])
  #os.system('cp memtraces/loop_array_add_INNERMOST_LN1_0.txt '+SIMULATOR_KERNEL)
  os.system('cp -r memtraces/ '+SIMULATOR_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_mem_alloc.txt '+SIMULATOR_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_mem_alloc.txt '+MAPPER_KERNEL)
  os.system('cp array_add_INNERMOST_LN1_PartPred_DFG.xml '+ MAPPER_KERNEL)

#############################################################################################################################################
  print('\nRunning Morpher_CGRA_Mapper\n')
  os.chdir(MAPPER_KERNEL)

  os.system('rm *.bin')
  os.system('mkdir binary')  
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem.json array_add_INNERMOST_LN1_mem_alloc.txt 8192 2 hycube_original_mem.json')
  os.system('python ../../../update_mem_alloc.py ../../../json_arch/hycube_original_updatemem_RC.json array_add_INNERMOST_LN1_mem_alloc.txt 8192 2 hycube_original_mem_RC.json')
  print('\nupdate memory allocation done!\n')
  os.system('../../../build/src/cgra_xml_mapper -d array_add_INNERMOST_LN1_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem.json -t HyCUBE_4REG > map_left.log')
  os.system('mv *.bin binary/left.bin')
  os.system('../../../build/src/cgra_xml_mapper -d array_add_INNERMOST_LN1_PartPred_DFG.xml -x 4 -y 4 -j hycube_original_mem_RC.json -t HyCUBE_4REG  > map_right.log')
  os.system('mv *.bin binary/right.bin')
  os.chdir(SIMULATOR_KERNEL)
  os.system('rm *.bin')  

  os.chdir(MAPPER_KERNEL)
  os.system('cp binary/*.bin '+ SIMULATOR_KERNEL)

##############################################################################################################################################
  print('\nRunning hycube_simulator\n')
  os.chdir(SIMULATOR_KERNEL)
  os.system('mv  array_add_INNERMOST_LN1_mem_alloc.txt mem_alloc.txt')
  os.system('python3 ../../scripts/duplicate_config.py')

  for invocations in range(0,num_memory_traces) :
    data_file = SIMULATOR_KERNEL + '/memtraces/loop_array_add_INNERMOST_LN1_' + str(invocations) + '.txt'
    os.system('python3 ../../scripts/skipdata.py --cubedata '+data_file)
    data_file_new = 'data_modi_' + str(invocations) + '.txt'
    os.system('cp data_modi.txt '+data_file_new)


  invocation = num_memory_traces // 4
  half_invocations = num_memory_traces % 4

  if invocation > 0 :
   for i in range(0,invocation) :
    os.system('../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str(i*4) +'.txt mem_alloc.txt 8 8 16384 data_modi_' + str((i*4 + 1)) + '.txt data_modi_' + str((i*4 + 2)) + '.txt data_modi_' + str((i*4 + 3)) +'.txt')
    out_file = 'dumped_raw_data_i' + str(i)
    os.system('cp dumped_raw_data.txt '+ out_file + '.txt')

  if half_invocations == 1 :
    os.system('../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384')
  
  if half_invocations == 2 :
    os.system('../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384 data_modi_'  + str((invocation*4 + 1)) +'.txt')

  if half_invocations == 3 :
    os.system('../../src/build/hycube_simulator duplicated_config.bin data_modi_' + str((invocation*4)) +'.txt mem_alloc.txt 8 8 16384 data_modi_'  + str((invocation*4 + 1))  + '.txt data_modi_' + str((invocation*4 + 2)) +'.txt')
	
  print('\nSimulation done! -> invocations = %d , half invocations = %d ,memory traces=%d\n' % (invocation,half_invocations,num_memory_traces))
#  print('\nSimulation done! -> memory traces=%d\n' % (num_memory_traces))

  #os.system('../../src/build/hycube_simulator *.bin loop_array_add_INNERMOST_LN1_0.txt array_add_INNERMOST_LN1_mem_alloc.txt')

def my_mkdir(dir):
    try:
        os.makedirs(dir) 
    except:
        pass

if __name__ == '__main__':
  main()
