#!/opt/python/bin/python3

# Module for getting arguments/inputs from user.
import argparse
# Used here for exiting script with status code.
import sys
# Module for sending commands to bash shell.
import subprocess
# Import ipaddress module for ease of working with IP addresses.
import ipaddress
# This module helps us to spawn multiple parallel threads.
from threading import Thread

class InventoryAudit(Thread):
    def __init__(self,IP):
        Thread.__init__(self)
        self.IP = IP

    def run(self):
        print("Running script on "+self.IP)
        inventory(self.IP)

def inventory(IP):
   try:
      command_1="ping -c 5 {0}".format(IP)
      ping=subprocess.getoutput(command_1)
      #print(ping)
      if "5 received" in ping or "4 received" in ping or "3 received" in ping:
         command_2="snmpget -v2c -c 75Pubm4t1cSNMP -OQv {0} .1.3.6.1.2.1.1.5.0".format(IP)
         name=subprocess.getoutput(command_2)
         #print(name)
         command_3="snmpget -v2c -c 75Pubm4t1cSNMP -OQv {0} .1.3.6.1.2.1.1.1.0".format(IP)
         full_model_out=subprocess.getoutput(command_3)
         #print(full_model_out)
         if "qfx5100" in full_model_out:
             model = "qfx5100"
         #elif "qfx5200" in full_model_out:
             #model = "qfx5200"
             result="""
{0}:
   hostname: {1}
   groups:
       - junos
   data:
       role: TOR
       model: {2}
""".format(name,IP,model)
             with open( 'inventory.yaml', 'a+' ) as out:
                 out.writelines(result)

   except Exception as e:
       print("ERROR:{0}".format(e))

def main():
   thread_list=[]
   for IP in ipaddress.ip_network('10.221.2.0/24'):
      audit=InventoryAudit(IP)
      thread_list.append(audit)
      audit.start()
   for thread in thread_list:
       thread.join()

if __name__ == '__main__':
   main()
