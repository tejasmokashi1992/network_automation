#!/usr/bin/python3
from nornir import InitNornir
from nornir.plugins.tasks.networking import netconf_get, netconf_capabilities, netconf_get_config
from rich import print
from xml.dom import minidom
import itertools
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from lxml import etree
from xmlhelp import strip_ns

nr = InitNornir(config_file="config.yaml")
junos = nr.filter(F(hostname="192.168.1.10"))

#def ipvzero(task):
#filtered = "<configuration><interfaces></interfaces></configuration>"
#filtered = "<configuration><vlans></vlans></configuration>"
#xpath = "//*[local-name()='vlans']"
#xpath = (".//host-name")
#filtered = "<configuration><system></system></configuration>"
#raw = task.run(task=netconf_get, path="/l2ng-l2ald-vlan-instance-information/l2ng-l2ald-vlan-instance-group/l2ng-l2rtb-vlan-name")

raw = junos.run(task=netconf_get)
#raw = junos.run(task=netconf_get, path=xpath, filter_type="xpath")
#raw = junos.run(task=netconf_get, path=filtered, filter_type="subtree")
#raw = junos.run(task=netconf_get_config)
#raw = junos.run(task=netconf_get_config, path=xpath)
#raw = junos.run(task=netconf_get_config, filter_type="subtree", path=filtered)

    #result = minidom.parseString(raw).toprettyxml()
    #inter = minidom.parseString(resulter).getElementsByTagName("name")
    #for x,y in zip(unicasts, inter):
      #  packets = x.firstChild.nodeValue
       # namers = y.firstChild.nodeValue
        #print(f"[green]{task.host}:[/green] Interfaces receiving packets: [u]{namers}[/u] (total:{packets})\n")
    #print(f"[green]******{task.host}******\n[/green]" + "\n" + result + "\n\n\n")
content = raw['TOR_1'].result
content = content.encode('utf-8')
type(content)
parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
et = etree.fromstring(content, parser=parser)
out = strip_ns(et)
out.xpath("//data/configuration/vlans/vlan")
#print_result(raw)
#def main():

    #junos = nr.filter(F(name="TOR_1")
 #   nr.run(task=ipvzero)

#if __name__ == '__main__':
   # main()
