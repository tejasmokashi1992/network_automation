#!/usr/bin/python3

from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.files import write_file

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)

#devices = nr.filter(F(platform="junos"))
devices = nr.filter(F(hostname="192.168.1.20"))

BACKUP_PATH = "/mnt/d/repo/Configs"

def Device_config(task, path):
    print(f"Collecting data from {task.host}")
    r = task.run(task=netmiko_send_command, command_string="show configuration | display set | no-more")
    task.run(task=write_file, content=r.result, filename=f"{path}/{task.host}.txt")

result = devices.run(name="Backup Device configurations", path=BACKUP_PATH, task=Device_config)
print_result(result, vars=["stdout"])
#print_result(result)
