#!/usr/bin/python3
import json
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import click

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


def audit(task, command, first_string):
    try:
       output = task.run(task=netmiko_send_command, command_string=command)
       #print_result(output)
       if first_string not in output.result:
           print("Error found on :{0}".format(task.host.hostname))
           with open( 'unconfigured_devices', 'a+' ) as audit_out:
              audit_out.write(task.host.hostname+"\n")
       else:
            print("Done Checking {0}".format(task.host.hostname))

    except Exception as e:
        print("ERROR:{0}".format(e))

def main():
    open("unconfigured_devices", "w").close()
    command = click.prompt("Enter the command in display set")
    first_string = click.prompt("Enter string you want to be matched")
    out=junos.run(task=audit, command=command, first_string=first_string, num_workers=20)
    #print_result(out)

if __name__ == '__main__':
    main()
