import os
import glob
import shutil
import pandas as pd
import time
import subprocess
import sys
import smtplib
import sendmail
import os
import sys
import time

def check_profiler():
    response = os.system("ping -c 1 192.168.2.27" )
    if response != 0 :
        print ("Error has occoured on the profiler, Lost connection.\n")
        print("Response code", response)
        time.sleep(10)



### NETLOG COMMANDS###
netlog_cmd1_start_GW1_I1 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StartNetworkCapture.sh "
netlog_cmd1_start_GW1_I2 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StartNetworkCapture_I2.sh "
netlog_cmd5_stop_GW1 = "echo \"jug@@d*%$\" |  /home/jugaad/jugaad/Malware/GW1/GW1_StopAndLogNWData.sh"

print("Start network capture")
### Start the Network Capture in GW1 and GW2 ###
#---------- Write the netlog commmands 
print("\n Trigger procmon remotely")

p = subprocess.Popen(["/usr/bin/pwsh",  "/home/jugaad/jugaad/Malware/GW1/startTest/protest.ps1", file],stdin=DEVNULL,stdout=sys.stdout)

p.communicate()
print("\n")
print("Procmon done")
print("Stopping the network capture\n")

time.sleep(20)
os.system("sshpass -p jugaad scp jugaad@192.168.2.27:c:/Profiler_OS_NW/OS_Data_csv/*.csv /home/jugaad/OS_DataFromProfiler/")

os.system ("sshpass -p jugaad scp jugaad@192.168.2.27:c:/Profiler_OS_NW/*.pid /home/jugaad/PID_DataFromProfiler/")


# ### Stop the network capture and transfer filer to GW1/NetworkData
# os.system(netlog_cmd5_stop_GW1)
