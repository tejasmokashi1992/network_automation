#!/opt/python/bin/python3

# Module for getting arguments/inputs from user.
import argparse
# Used here for exiting script with status code.
import sys
# Module for sending commands to bash shell.
import subprocess
# Import ipaddress module for ease of working with IP addresses.
import ipaddress


def inventory():
   for IP in ipaddress.ip_network('10.221.2.0/24'):
      command_1="ping -c 5 {0}".format(IP)
      ping=subprocess.getoutput(command_1)
      #print(ping)
      if "5 received" in ping or "4 received" in ping or "3 received" in ping:
         command_2="snmpget -v2c -c SNMP_COMMUNITY -OQv {0} .1.3.6.1.2.1.1.5.0".format(IP)
         name=subprocess.getoutput(command_2)
         #print(name)
         command_3="snmpget -v2c -c SNMP_COMMUNITY -OQv {0} .1.3.6.1.2.1.1.1.0".format(IP)
         full_model_out=subprocess.getoutput(command_3)
         #print(full_model_out)
         if "qfx5100" in full_model_out:
            result="""
{0}:
   hostname: {1}
   groups:
       - junos
   data:
       role: TOR
       model: qfx5100
""".format(name,IP)
         with open( 'inventory.yaml', 'a+' ) as out:
            out.writelines(result)

def main():
   inventory()

if __name__ == '__main__':
   main()
