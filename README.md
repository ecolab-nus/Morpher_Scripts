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
# How to run?

 1) Build all three tools before running the scripts

 2) Use python3 virtual environment to run the script
 https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/

 first time: python3 -m venv morpher_env
 next: source morpher_env/bin/activate

 3) Set MORPHER_HOME directory as an environment variable (Ex: export MORPHER_HOME=/home/dmd/Workplace/Morphor/github_ecolab_repos)

 4) python run_morpher.py

run_morpher.py contains the pedometer application kernel. 
 
 Final Output should be: 
	Matches ::557, Mismatches::20 
 TODO:Automate memory allocation copy from mem_alloc.txt to mem.json

run_morpher_array_add.py
 
 Final Output should be:
        Matches :: 241, Mismatches::0
 Make sure to run this before making any major change to the repos

