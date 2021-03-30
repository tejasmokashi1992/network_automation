#!/usr/bin/python3

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.filter import F
import click
from rich import print

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
           print("[bright_green] Done checking: {0} [/bright_green]".format(task.host.hostname))
       else:
           print("[bright_red] Desired string not found on: {0} [/bright_red]".format(task.host.hostname))
           with open( 'non_compliant_devices', 'a+' ) as audit_out:
               audit_out.write(task.host.hostname+"\n")

    except Exception as e:
        print("Error encounterd on: {0}".format(task.host.hostname))
        print("ERROR:{0}".format(e))

def main():
    nr = InitNornir(config_file="config.yaml")
    open("non_compliant_devices", "w").close()
    print("\n"+"**********"+"[u cyan]Welcome to Network Audit Script[/u cyan]"+"**********"+"\n\n")

    dev_role = click.prompt(click.style("Enter device type for audit:", fg='yellow'),
            type=click.Choice(['TOR', 'corerouter', 'coreswitch', 'all'],
                case_sensitive=True))
    command = click.prompt(click.style("Enter the desired command ", fg='bright_magenta'))
    find_string = click.prompt(click.style("Enter string or list of comma seperated strings to be matched", fg='bright_blue')).split(',')

    print(50*"#")
    if dev_role == "all":
        junos = nr.filter(F(platform="junos"))
        out = junos.run(task=audit, command=command, find_string=find_string)
        print(50*"#")
    else:
        junos = nr.filter(F(role="{0}".format(dev_role)))
        out = junos.run(task=audit, command=command, find_string=find_string)
        print(50*"#")
    print_result(out)

if __name__ == '__main__':
    main()
