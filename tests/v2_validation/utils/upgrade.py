import subprocess
import random
import os
import sys
import re
import time

RESOURCES_SUBDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'resources')
CLI_DIR = os.path.dirname(os.path.realpath(__file__))
envfilepath = CLI_DIR + "/envfile.txt"
print(envfilepath)
def getenvidarray():
    # Method to get the list of environments
    try:
       time.sleep(4)
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
    print(envarray)
    return(envarray)

def getstackidarray(envid):
    
    # Method to get the stackid info given envid 
    command = CLI_DIR + "/rancher --env=" + envid + " stack ls --system"
    print(command)
    output = subprocess.check_output(command, shell=True,
                                     stderr=subprocess.PIPE)
    cmdoutput = output.decode('utf-8')
    stackrowentry = cmdoutput.split('\n')
    #print("******* STACK ENTRY *********")
    #print(stackrowentry)
    stackdict = {}
    for item in stackrowentry:
        stackrow = re.findall('\w+', item)
        if(len(stackrow) > 2):
          if(stackrow[1] == "network") or (stackrow[1] == "ipsec") or (stackrow[1] == "healthcheck") or (stackrow[1] == "scheduler"):
            stackdict.update({stackrow[1]:str(stackrow[0])})
    #print(stackdict)
    return(stackdict)

# Get environment list
#envlist = getenvidarray()
#f = open(envfilepath, "w")
#for env in envlist:
#   f.write(env)
#   f.write('\n')
#f.close()

def run_command(command):
    print(command)
    for i in range(3):
        try:
           cmdoutput = subprocess.check_output(command, shell=True,
                              stderr=subprocess.STDOUT)
           print(cmdoutput)
           break
        except subprocess.CalledProcessError as e:
           print ("Retrying")
           time.sleep(5)


testarray = []
fp = open(envfilepath, "r")
testarray = fp.read().split('\n')
testarray = list(filter(None, testarray))
print("Array after file read")
print(testarray)   
print(len(testarray))

upgradedenvlist = [] 
for envid in testarray:
    print("Environmnent ID is")
    print("************** Upgrading ENV **********")
    print(envid)
    time.sleep(3)
    stackdict = getstackidarray(envid)
    stackname = "stack" + str(random.randint(0, 1000000))
    networkservicesid = stackdict['network']
    print(networkservicesid)
    rancherupnetworkcmd = CLI_DIR + "/rancher --env=" + envid + " catalog upgrade " + \
                              "library:infra*network-services:29" + " --confirm --stack " + networkservicesid
    ipsecid = stackdict['ipsec']
    print(ipsecid)
    rancherupipseccmd = CLI_DIR + "/rancher --env=" + envid + " catalog upgrade " + \
                          "library:infra*ipsec:18" + " --confirm --stack " + ipsecid
    schedulerid = stackdict['scheduler']
    print(schedulerid)
    rancherupschedulercmd = CLI_DIR + "/rancher --env=" + envid + " catalog upgrade " + \
                        "library:infra*scheduler:13" + " --confirm --stack " + schedulerid
    healthcheckid = stackdict['healthcheck']
    print(healthcheckid)
    rancheruphealthcheckcmd = CLI_DIR + "/rancher --env=" + envid + " catalog upgrade "+ \
                   "library:infra*healthcheck:7"+ " --confirm --stack " + healthcheckid
    print(rancherupnetworkcmd)
    print(rancherupipseccmd)
    print(rancherupschedulercmd)
    print(rancheruphealthcheckcmd)
    print(".......Upgrading Network Services ......")
    run_command(rancherupnetworkcmd)
    time.sleep(3)
    print(".......Upgrading Ipsec ......")
    run_command(rancherupipseccmd)
    time.sleep(3)
    print(".......Upgrading Scheduler ......")
    run_command(rancherupschedulercmd)
    time.sleep(2)
    print(".......Upgrading Healthcheck ......")
    run_command(rancheruphealthcheckcmd)
    upgradedenvlist.append(envid)

print("Upgraded env list")
print(upgradedenvlist)



      
