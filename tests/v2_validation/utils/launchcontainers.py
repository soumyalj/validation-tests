import subprocess
import random
import os
import sys
import time

RESOURCES_SUBDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'resources')
CLI_DIR = os.path.dirname(os.path.realpath(__file__))

envfilepath = CLI_DIR + "/envfile1.txt"
print(envfilepath)

itercount = int(sys.argv[1])


def getenvidarray():
    # Method to get the list of environments
    command = CLI_DIR + "/rancher env ls"
    try:
        output = subprocess.check_output(command, shell=True,
                                     stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' "
                           "return with error (code {}): {}".format(e.cmd,
                           e.returncode, e.output))    
    cmdoutput = output.decode('utf-8')
    print(cmdoutput)
    enventry = cmdoutput.split('\n')
    envarray = []
    for item in enventry:
        print(item)
        enventry = item.split(' ')
        print(enventry[0])
        idtext = 'ID'
        if(enventry[0] != idtext) and (enventry[0] != ''):
            envarray.append(enventry[0])
    print(envarray)
    return(envarray)

testarray = []
fp = open(envfilepath, "r")
testarray = fp.read().split('\n')
envlist = list(filter(None, testarray))
print("Array after file read")
print(envlist)
print(len(envlist))
# Get environment list
#envlist = getenvidarray()
#envlist = ['1a1027','1a1028', '1a1029','1a1030', '1a7']

for envid in envlist:
    print("Environmnent ID is")
    print(envid)
    stackname = "stack" + str(random.randint(0, 1000000))
    # Create stack with services and Lbs pointing to the services
    #try:
    #    rancherupcmd = CLI_DIR + "/rancher --env="+envid+" up -d " \
    #                   "--file="+RESOURCES_SUBDIR+\
    #                   "/dc_stack.yml "+ "--rancher-file="+RESOURCES_SUBDIR+\
    #                   "/rc_stack.yml -s " + stackname
    #    print(rancherupcmd)
    #    subprocess.check_output(rancherupcmd, shell=True,
    #                            stderr=subprocess.STDOUT)
    #except subprocess.CalledProcessError as e:
    #    raise RuntimeError("command '{}' "
    #                       "return with error (code {}): {}".format(e.cmd,
    #                       e.returncode, e.output))
    # Create stack with only services
    for i in range(itercount):
        print(i)
        #stackname = "stack" + str(random.randint(0, 1000000))
        stackname = "afterinfraupgstack"
        try:
           rancherupcmd = CLI_DIR + "/rancher --env="+envid+" up -d  \
                       --file="+RESOURCES_SUBDIR+\
                       "/dc_stack.yml "+ "--rancher-file="+RESOURCES_SUBDIR+\
                       "/rc_stack.yml -s " + stackname
           print(rancherupcmd)
           subprocess.check_output(rancherupcmd, shell=True,
                                   stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
           raise RuntimeError("command '{}' "
                           "return with error (code {}): {}".format(e.cmd,
                           e.returncode, e.output))
        time.sleep(10)

    time.sleep(10)

