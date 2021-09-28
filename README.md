# Morpher_Scripts
 
 Single script to run all three tools (Morpher_DFG_Generator, Morpher_CGRA_Mapper, hycube_simulator) to verify the functionality.
 
##########################################################
# Directory Structure:
 Morpher Home:
 
     -Morpher_DFG_Generator
     -Morpher_CGRA_Mapper
     -hycube_simulator
     -Morpher_Scripts

###########################################################
# Installing the software stack 

## Build dependencies: 

DFG Generator requires LLVM 10.0.0 and CGRA Mapper requires nlohmann-JSON libraries. 

Steps to install LLVM, clang, polly on Ubuntu: 

    Read https://llvm.org/docs/GettingStarted.html follow https://github.com/llvm/llvm-project 

    git clone https://github.com/llvm/llvm-project.git 

    git checkout <correct version>              (current version: llvm10.0.0) 

    cd llvm-project 

    mkdir buildecho $P 

    cd build 

    cmake -DLLVM_ENABLE_PROJECTS='polly;clang' -G "Unix Makefiles" ../llvm 

    make -j4 

    sudo make install 

Important points: 

    make sure to checkout correct version before building (current version: llvm10.0.0) 

    better to use gold linker instead of ld if you face memory problem while building: https://stackoverflow.com/questions/25197570/llvm-clang-compile-error-with-memory-exhausted 

    don't use release type use default debug version (will take about 70GB disk space) 

 

JSON: 

    https://blog.csdn.net/jiaken2660/article/details/105155257 

    git clone https://github.com/nlohmann/json.git 

    mkdir build 

    cd build 

    cmake .. 

    make -j2 

    sudo make install 

 

## DFG Generator 

    cd <Morpher_HOME> 

    git clone https://github.com/ecolab-nus/Morpher_DFG_Generator.git 

    cd Morpher_DFG_Generator 

    git checkout stable 

    mkdir build 

    cd build 

    cmake .. 

    make all 

## CGRA Mapper 

    cd <Morpher_HOME> 

    git clone https://github.com/ecolab-nus/Morpher_CGRA_Mapper.git 

    cd Morpher_CGRA_Mapper 

    git checkout stable 

    mkdir build 

    cd build 

    cmake .. 

    make all –j 

## Simulator (hycube_simulator) 

    cd <Morpher_HOME> 

    git clone https://github.com/ecolab-nus/hycube_simulator.git 

    Cd hycube_simulator/src 

    mkdir build 

    cd build 

    cmake .. 

    make all –j 

 

# Getting Started 

 

## Scripts 

Morpher provides python scripts to invoke all three tools (DFG generator, Mapper and Simulator) interactively.   

    cd <Morpher_HOME> 

    git clone https://github.com/ecolab-nus/Morpher_Scripts.git 

    cd Morpher_Scripts 

    Use python3 virtual environment to run the scripts https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/ 

    - First time 

        -mkdir environments 

        -cd environments 

        -python3 -m venv project_env 

    - source project_env/bin/activate 

    Set MORPHER_HOME directory as an environment variable  

    Export MORPHER_HOME = <Morpher_HOME> 

    -E.g., export MORPHER_HOME=/home/Workplace/Morphor/github_ecolab_repos 

    python run_morpher_<kernel_name>.py 

    Expected output of run_morpher_array_add.py 
    - Matches: 241 Mismatches: 0

 

  ## Explanation of run_morpher_array_add.py. 


    Line 36-53: DFG Generator 

    Line 41: running run_pass.sh script (DFG generation, Data Placement and Instrumentation) 

    Line 42: convert DFG dot file to pdf file  

    Line 49: Running instrumented executable for generating data memory content.  

    Line 50: Copy data memory content file to folder in simulator 

    Line 51: Copy data allocation file to folder in simulator 

    Line 52: Copy DFG xml to folder in mapper 

    Line 55-65: Mapper 

    Line 59: Running mapper 

    Line 65: Copy generated CGRA configuration binary file to simulator 

    Line 68-71: Simulator 

    Line 71: Running simulator 

 

 
