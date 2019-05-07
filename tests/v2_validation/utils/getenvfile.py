import subprocess
import random
import os
import sys
import re
import time

CLI_DIR = os.path.dirname(os.path.realpath(__file__))
envfilepath = CLI_DIR + "/envfile.txt"
print(envfilepath)

def getenvidarray():
    # Method to get the list of environments
    try:
       time.sleep(5)
       command = CLI_DIR + "/rancher env ls"
       output = subprocess.check_output(command, shell=True,
                                     stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' "
                           "return with error (code {}): {}".format(e.cmd,
                           e.returncode, e.output))
    cmdoutput = output.decode('utf-8')
    enventry = cmdoutput.split('\n')
    envarray = []
    for item in enventry:
        enventry = item.split(' ')
        print(enventry[0])
        idtext = 'ID'
        if(enventry[0] != idtext) and (enventry[0] != ''):
            envarray.append(enventry[0])
    print("My array")
    print(envarray)
    print(len(envarray))
    return(envarray)

# Get environment list
envlist = getenvidarray()
f = open(envfilepath, "w")
for env in envlist:
   f.write(env)
   f.write('\n')
f.close()

