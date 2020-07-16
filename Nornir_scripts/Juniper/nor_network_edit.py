#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import click
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

#junos = nr.filter(F(platform="junos"))
#junos = nr.filter(F(hostname="192.168.1.10"))
#junos = nr.filter(F(name="CR_1"))

def configuration(task, filepath):
  try:
       #output = task.run(task=netmiko_send_config, config_file="/home/tejas/day-one-net-toolkit/network_config.txt")
       output = task.run(task=napalm_configure, filename=filepath)
       print("Config done for device :{0}".format(task.host.hostname))

  except Exception as e:
       print("ERROR:{0}".format(e))
       print("Device config not done:{0}".format(task.host.hostname))
       #exc_info = sys.exc_info()
       #traceback.print_exception(*exc_info)

def main():
    dev_role = click.prompt("Please enter device type for audit:",
            type=click.Choice(['TOR', 'corerouter', 'coreswitch', 'all'],
                case_sensitive=True))
    filepath = click.prompt("Enter the config file path", type=str)
    if dev_role == "all":
       junos = nr.filter(F(platform="junos"))
       out=junos.run(task=configuration, filepath=filepath, num_workers=20)
    else:
       junos = nr.filter(F(role="{0}".format(dev_role)))
       out=junos.run(task=configuration, filepath=filepath, num_workers=20)
    print_result(out)

if __name__ == '__main__':
    main()
