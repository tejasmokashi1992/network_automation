#!/usr/bin/python3
import json
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import ipaddress

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)


def check_ping(IP):
     try:
        if ipaddress.ip_address(IP) not in ipaddress.ip_network('10.90.0.0/16'):
            print("Server IP {0} is not in range for TY6 DC servers".format(IP))
        else:
            SWITCH = nr.filter(F(hostname="10.91.2.4"))
            PING = SWITCH.run(task=napalm_ping, dest=IP)
            if "success" in PING['CS_1'].result:
                print("=======================================================")
                print("Server IP {0} is Pingable".format(IP))
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
                       check_lacp_lldp(INTERFACE,MAC)
            else:
                print("Server IP {0} NOT Pingable".format(IP))
                pass
     except Exception as e:
         print("ERROR:{0}".format(e))


def check_lacp_lldp(INTERFACE,MAC):
     try:
       SWITCH = nr.filter(F(hostname="10.91.2.4"))
       LACP = SWITCH.run(task=netmiko_send_command, command_string="show lacp interface {0} | display json | no-more".format(INTERFACE))
       LACP_DICT = json.loads(LACP['CS_1'].result)
       LACP_INTERFACE = LACP_DICT["lacp-interface-information-list"][0]["lacp-interface-information"][0]["lag-lacp-state"][0]["name"][0]["data"]
       LLDP = SWITCH.run(task=netmiko_send_command, command_string="show lldp neighbors interface {0} | display json | no-more".format(LACP_INTERFACE))
       LLDP_DICT = json.loads(LLDP['CS_1'].result)
       LLDP_NEIGHBOR = LLDP_DICT["lldp-neighbors-information"][0]["lldp-neighbor-information"][0]["lldp-remote-management-address"][0]["data"]
       login_next(MAC,LLDP_NEIGHBOR)
     except Exception as e:
         print("ERROR:{0}".format(e))


def login_next(MAC,LLDP_NEIGHBOR):
    try:
        print("Connection to TOR: {0}".format(LLDP_NEIGHBOR))
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


        print("Server is on device: {0}".format(DEVICE))
        print("Server is on interface: {0}".format(SERVER_INTERFACE))
        print("Server VLAN TAG: {0}".format(VLAN_TAG))
        print("Server RU Number is: {0}".format(DESC))
        print("=======================================================")

    except Exception as e:
        print("ERROR:{0}".format(e))


def main():
    with open('Server_IP_List') as f:
        server_list = f.read().splitlines()

    for IP in server_list:
        check_ping(IP)


if __name__ == '__main__':
    main()
