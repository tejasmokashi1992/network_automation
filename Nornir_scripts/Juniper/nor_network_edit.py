#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_config
#from nornir_scrapli.tasks import send_configs_from_file
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import click
from rich import print

#junos = nr.filter(F(platform="junos"))
#junos = nr.filter(F(hostname="192.168.1.10"))
#junos = nr.filter(F(name="CR_1"))

def configuration(task, filepath):
  try:
     #output = task.run(task=netmiko_send_config, config_file=filepath)
     #output = task.run(task=send_configs_from_file, file=filepath)
     output = task.run(task=napalm_configure, filename=filepath)
     print("[bright_green]Config done for device: {0}[/bright_green]".format(task.host.hostname))
  except Exception as e:
     print("ERROR:{0}".format(e))
     print("[bright_red]Error while configuring device: {0}[bright_red]".format(task.host.hostname))

def main():
    nr = InitNornir(config_file="config.yaml")
    print("\n"+"**********"+"[u cyan]Welcome to Network Edit Script[/u cyan]"+"**********"+"\n\n")

    dev_role = click.prompt(click.style("Enter device type:", fg='yellow'),
            type=click.Choice(['TOR', 'corerouter', 'coreswitch', 'all'],
                case_sensitive=True))
    filepath = click.prompt(click.style("Enter the config file path", fg='bright_magenta'), type=str)

    print(50*"#")
    if dev_role == "all":
       junos = nr.filter(F(platform="junos"))
       out=junos.run(task=configuration, filepath=filepath, num_workers=50)
       print(50*"#")
    else:
       junos = nr.filter(F(role="{0}".format(dev_role)))
       out=junos.run(task=configuration, filepath=filepath, num_workers=50)
       print(50*"#")
    print_result(out)

if __name__ == '__main__':
    main()
