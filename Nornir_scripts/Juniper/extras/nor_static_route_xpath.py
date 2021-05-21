#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import netconf_get, netconf_capabilities, netconf_get_config
from rich import print
from xml.dom import minidom
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from lxml import etree


def static_route(task):

    raw = task.run(task=netconf_get)
    result = raw.result
    element = minidom.parseString(result).getElementsByTagName("static")
    #result = minidom.parseString(raw).toprettyxml()
    for i in element:
        name_list = i.getElementsByTagName("name")
        next_hop_list = i.getElementsByTagName("next-hop")
        print(f"############# {task.host} #############")
        for x, y in zip(name_list, next_hop_list):
            name = x.firstChild.nodeValue
            next_hop = y.firstChild.nodeValue
            print(f"{name} Next_hop: [green]{next_hop}[/green]")
        print("#" * 35)
    #print_result(raw)

def main():
    nr = InitNornir(config_file="config.yaml")
    junos = nr.filter(F(hostname="192.168.1.20"))
    out = junos.run(task=static_route)
    #print_result(out)

if __name__ == '__main__':
    main()
