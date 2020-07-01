#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
#import sys
#import traceback

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)

junos = nr.filter(F(platform="junos"))
#junos = nr.filter(F(hostname="192.168.1.10"))
#junos = nr.filter(F(name="CR_1"))

def configuration(task):
  try:
       #output = task.run(task=netmiko_send_config, config_file="/home/tejas/day-one-net-toolkit/network_config.txt")
       output = task.run(task=napalm_configure, filename="/home/tejas/day-one-net-toolkit/network_config.txt")
       print("Config done for device :{0}".format(task.host.hostname))

  except Exception as e:
       print("ERROR:{0}".format(e))
       print("Device not done:{0}".format(task.host.hostname))
       #exc_info = sys.exc_info()
       #traceback.print_exception(*exc_info)

def main():
    out=junos.run(task=configuration, num_workers=10)
    #print_result(out)

if __name__ == '__main__':
    main()
