#!/usr/bin/python3

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command, napalm_cli
#from nornir_scrapli.tasks import send_command as scrapli_send_command
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

#junos = nr.filter(F(platform="junos") & F(role="TOR"))
#junos = nr.filter(F(hostname="192.168.1.10"))
#junos = nr.filter(F(name="CR_1"))

def audit(task, command, find_string):
    try:
       output = task.run(task=netmiko_send_command, command_string=command)
       #output = task.run(task=scrapli_send_command, command=command)
       #output = task.run(task=napalm_cli, commands=list(command))
       #print_result(output)
       if all(element in output.result for element in find_string):
           print("Done Checking: {0}".format(task.host.hostname))
       else:
           print("Desired string not found on: {0}".format(task.host.hostname))
           with open( 'unconfigured_devices', 'a+' ) as audit_out:
               audit_out.write(task.host.hostname+"\n")

    except Exception as e:
        print("Error encounterd on: {0}".format(task.host.hostname))
        print("ERROR:{0}".format(e))
        
def main():
    open("unconfigured_devices", "w").close()
    dev_role = click.prompt("Please enter device type for audit:",
            type=click.Choice(['TOR', 'corerouter', 'coreswitch', 'all'],
                case_sensitive=True))
    command = click.prompt("Enter the command in display set format")
    find_string = (click.prompt("Enter single string or comma(,) seperated string you want to be matched")).split(',')
    if dev_role == "all":
        junos = nr.filter(F(platform="junos"))
        out = junos.run(task=audit, command=command, find_string=find_string, num_workers=20)
    else:
        junos = nr.filter(F(role="{0}".format(dev_role)))
        out = junos.run(task=audit, command=command, find_string=find_string, num_workers=20)
    #print_result(out)

if __name__ == '__main__':
    main()
