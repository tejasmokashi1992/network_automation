#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import json

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
#junos = nr.filter(F(hostname="10.91.2.11"))

def audit(task):
    try:
       output = task.run(task=netmiko_send_command, command_string="show configuration | display set | match archival")
       #print_result(outout)
       if "transfer-on-commit" not in output.result or "archive-sites" not in output.result:
           print("Error found on :{0}".format(task.host.hostname))
           with open( 'unconfigured_devices', 'a+' ) as audit_out:
              audit_out.write(task.host.hostname+"\n")
       else:
            print("Done Checking {0}".format(task.host.hostname))

    except Exception as e:
        print("ERROR:{0}".format(e))

def main():
    out=junos.run(task=audit, num_workers=20)

if __name__ == '__main__':
    main()
