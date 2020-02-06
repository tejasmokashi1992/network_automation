#!/opt/python/bin/python3

from netmiko import ConnectHandler
from getpass import getpass
import json
import argparse
#username = input('Enter your SSH username: ')
password = getpass()

def audit(IP):
        global INTERFACE
        global DEVICE
        global MAC
        ip_address_of_device = DEVICE
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': 'tejas.mokashi',
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            PING = net_connect.send_command('ping {0} count 5'.format(str(IP)))
            if "5 packets received" in PING or "4 packets received" in PING or "3 packets received" in PING:
                print("Server IP is Pingable")
                ARP = net_connect.send_command('show arp no-resolve | match {0}'.format(IP))
                ARP = ARP.split()
                MAC = ARP[0]
                INTERFACE = ARP[3][:-3][1:]
                check_lacp_lldp()
                net_connect.disconnect()
            else:
                print("Server IP NOT Pingable")
                pass
        except Exception as e:
            print("ERROR:{0}".format(e))


def check_lacp_lldp():
        global INTERFACE
        global DEVICE
        global lldp_neighbor
        ip_address_of_device = DEVICE
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': 'tejas.mokashi',
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            #----------------------------------------------------------------------------------------
            LACP = net_connect.send_command('show lacp interface {0} | display json | no-more'.format(INTERFACE))
            with open( 'lacp.json', 'w' ) as lacp_output:
                lacp_output.write(LACP+"\n")
            with open('lacp.json', 'r' ) as f:
                lacp_json = f.read()
            lacp_dict = json.loads(lacp_json)
            #print(lacp_json)
            #print(lacp_dict)
            lacp_interface = lacp_dict["lacp-interface-information-list"][0]["lacp-interface-information"][0]["lag-lacp-state"][0]["name"][0]["data"]
            #----------------------------------------------------------------------------------------
            LLDP = net_connect.send_command('show lldp neighbors interface {0} | display json | no-more'.format(lacp_interface))
            with open( 'lldp.json', 'w' ) as lldp_output:
                lldp_output.write(LLDP+"\n")
            with open('lldp.json', 'r' ) as f:
                lldp_json = f.read()
            lldp_dict = json.loads(lldp_json)
            #print(lldp_json)
            #print(lldp_dict)
            lldp_neighbor = lldp_dict["lldp-neighbors-information"][0]["lldp-neighbor-information"][0]["lldp-remote-management-address"][0]["data"]
            #----------------------------------------------------------------------------------------
            login_next_device()
            net_connect.disconnect()
        except Exception as e:
            print("ERROR:{0}".format(e))


def login_next_device():
        global lldp_neighbor
        global MAC
        global DEVICE
        global INTERFACE
        ip_address_of_device = lldp_neighbor
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': 'tejas.mokashi',
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            print("Connection to device: {0}".format(lldp_neighbor))
            ETHER = net_connect.send_command('show ethernet-switching table | match {0}'.format(MAC))
            ETHER = ETHER.split()
            INTERFACE_ETHER = ETHER[4][:-2]
            LLDP_CHECK = net_connect.send_command('show lldp neighbors | match {0}'.format(INTERFACE_ETHER))
            if INTERFACE_ETHER in LLDP_CHECK:
                DEVICE = lldp_neighbor[:]
                INTERFACE = INTERFACE_ETHER[:]
                check_lacp_lldp()
            else:
                VLAN = net_connect.send_command('show configuration interfaces {0} | display json | no-more'.format(INTERFACE_ETHER))
                print("Server is on interface: {0}".format(INTERFACE_ETHER))
                with open( 'vlan.json', 'w' ) as vlan_output:
                    vlan_output.write(VLAN+"\n")
                with open('vlan.json', 'r' ) as f:
                    vlan_json = f.read()
                vlan_dict = json.loads(vlan_json)
                #print(lacp_json)
                #print(lacp_dict)
                vlan_tag = vlan_dict["configuration"][0]["interfaces"][0]["interface"][0]["apply-groups"][0]["data"]
                print("Server is tagged with this group: {0}".format(vlan_tag))
        except Exception as e:
            print("ERROR:{0}".format(e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    args = parser.parse_args()
    ip=args.ip

    #with open('test_device') as f:
    #    device_list = f.read().splitlines()
    #    #print(device_list)
    #for device in device_list:
    audit(ip)

DEVICE="10.91.2.4"
MAC=""
INTERFACE=""
lldp_neighbor=""


if __name__ == '__main__':
    main()
