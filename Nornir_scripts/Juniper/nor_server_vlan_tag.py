#!/usr/bin/python3

import json
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
import datetime as dt
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from pprint import pprint
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import argparse


nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)


def check_ping(IP, RACK_NUM, RU_NUM):
     global INTERFACE
     global CORE_SW
     global MAC
     try:
        if IP[0:5] != "10.90":
            print("Mentiond IP is not in range for TY6 DC servers")
        else:
            SWITCH = nr.filter(F(hostname=CORE_SW))
            PING = SWITCH.run(task=netmiko_send_command, command_string="ping {0} count 5".format(IP))
            if "5 packets received" in PING['CS_1'].result or "4 packets received" in PING['CS_1'].result:
                print("Server IP is Pingable")
                ARP = SWITCH.run(task=napalm_get, getters=["arp_table"])
                for cs_name in ARP.keys():
                    CS_NAME = cs_name
                    #print(CS_NAME)

                ARP_LIST = ARP[CS_NAME].result['arp_table']
                for i, j in enumerate(ARP_LIST):
                    ALL_MAC = (j['mac'])
                    ALL_INTERFACE = (j['interface'])
                    ALL_IP = (j['ip'])
                    if ALL_IP == IP:
                       INTERFACE = ALL_INTERFACE.split()[1][1:][:-3]
                       MAC = ALL_MAC
                       check_lacp_lldp(RACK_NUM, RU_NUM)
            else:
                print("Server IP NOT Pingable")
                pass
     except Exception as e:
         print("ERROR:{0}".format(e))


def check_lacp_lldp(RACK_NUM, RU_NUM):
     global INTERFACE
     global LLDP_NEIGHBOR
     global CORE_SW
     global MAC
     try:
       SWITCH = nr.filter(F(hostname=CORE_SW))
       LACP = SWITCH.run(task=netmiko_send_command, command_string="show lacp interface {0} | display json | no-more".format(INTERFACE))
       LACP_DICT = json.loads(LACP['CS_1'].result)
       LACP_INTERFACE = LACP_DICT["lacp-interface-information-list"][0]["lacp-interface-information"][0]["lag-lacp-state"][0]["name"][0]["data"]
       LLDP = SWITCH.run(task=netmiko_send_command, command_string="show lldp neighbors interface {0} | display json | no-more".format(LACP_INTERFACE))
       LLDP_DICT = json.loads(LLDP['CS_1'].result)
       LLDP_NEIGHBOR = LLDP_DICT["lldp-neighbors-information"][0]["lldp-neighbor-information"][0]["lldp-remote-management-address"][0]["data"]
       login_next(RACK_NUM, RU_NUM)
     except Exception as e:
         print("ERROR:{0}".format(e))


def login_next(RACK_NUM, RU_NUM):
    global LLDP_NEIGHBOR
    global MAC
    global INTERFACE
    try:
        print("Connection to device: {0}".format(LLDP_NEIGHBOR))
        HOST = "TOR_"+ str(RACK_NUM)
        RACK_IP = nr.inventory.hosts[HOST].hostname
        SWITCH = nr.filter(F(hostname=LLDP_NEIGHBOR))
        MAC_TABLE = SWITCH.run(task=napalm_get, getters=["mac_address_table"])
        for device in SWITCH.inventory.hosts.keys():
            DEVICE = device
            #print(DEVICE)

        MAC_LIST = MAC_TABLE[DEVICE].result['mac_address_table']
        for i, j in enumerate(MAC_LIST):
            ALL_MAC = (j['mac'])
            ALL_INTERFACE = (j['interface'])
            if ALL_MAC == MAC:
               SERVER_INTERFACE = ALL_INTERFACE[:-2]

        INT_INFO = SWITCH.run(task=netmiko_send_command, command_string="show configuration interfaces {0} | display json | no-more".format(SERVER_INTERFACE))
        INT_INFO_DICT = json.loads(INT_INFO[DEVICE].result)
        VLAN_TAG = INT_INFO_DICT["configuration"][0]["interfaces"][0]["interface"][0]["apply-groups"][0]["data"]
        DESC = INT_INFO_DICT["configuration"][0]["interfaces"][0]["interface"][0]["description"][0]["data"]

        if LLDP_NEIGHBOR == RACK_IP:
            print("Server is on device: {0}".format(HOST))
            print("Server is on interface: {0}".format(SERVER_INTERFACE))
            print("Server VLAN TAG: {0}".format(VLAN_TAG))
            print("Server RU Number is: {0}".format(DESC))
            #print("Server" RU Number user provided: {0}").format(RU_NUM)
        else:
            print("Server is not on: {0}".format(HOST))
            print("Server is on device: {0}".format(DEVICE))
            print("Server is on interface: {0}".format(SERVER_INTERFACE))
            print("Server VLAN TAG: {0}".format(VLAN_TAG))
            print("Server RU Number is: {0}".format(DESC))
            #print("Server" RU Number user provided: {0}").format(RU_NUM)

    except Exception as e:
        print("ERROR:{0}".format(e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--rack_num')
    parser.add_argument('--ru_num')
    args = parser.parse_args()
    ip=args.ip
    rack_num=args.rack_num
    ru_num=args.ru_num
    check_ping(ip, rack_num, ru_num)


CORE_SW="10.91.2.4"
MAC=""
INTERFACE=""
LLDP_NEIGHBOR=""


if __name__ == '__main__':
    main()


'''

# ./nor_server_vlan_tag.py* --ip 10.90.130.104 --rack_num 631 --ru_num RU25
Server IP is Pingable
Connection to device: 10.91.2.11
Server is on device: TOR_631
Server is on interface: ae18
Server VLAN TAG: hypervisor-bond-trunk-vlan-all
Server RU Number is: AE-forRack631-RU18

# ./nor_server_vlan_tag.py* --ip 10.90.130.104 --rack_num 632 --ru_num RU25
Server IP is Pingable
Connection to device: 10.91.2.11
Server is not on: TOR_632
Server is on device: TOR_631
Server is on interface: ae18
Server VLAN TAG: hypervisor-bond-trunk-vlan-all
Server RU Number is: AE-forRack631-RU18

# ./nor_server_vlan_tag.py* --ip 10.51.130.104 --rack_num 631 --ru_num RU25
Mentiond IP is not in range for TY6 DC servers

# ./nor_server_vlan_tag.py* --ip 10.90.131.104 --rack_num 632 --ru_num RU25
Server IP NOT Pingable

'''