#!/usr/bin/python3
import json
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import re

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)

def check_tag(RACK_NUM, RU_NUM):
    try:
        HOST = "TOR_"+ (RACK_NUM)
        TOR_IP = nr.inventory.hosts[HOST].hostname
        SWITCH = nr.filter(F(hostname=TOR_IP))
        RU_CONF = SWITCH.run(task=netmiko_send_command, command_string="show configuration | display set | match RU{0}".format(RU_NUM))
        CONF_LIST = RU_CONF[HOST].result.split()
        subs = 'ae'
        # using re + search()
        # to get string with substring
        RES = [x for x in CONF_LIST if re.search(subs, x)]
        SERVER_INTERFACE = RES[0]

        INT_INFO = SWITCH.run(task=netmiko_send_command, command_string="show configuration interfaces {0} | display json | no-more".format(SERVER_INTERFACE))
        INT_INFO_DICT = json.loads(INT_INFO[HOST].result)
        VLAN_TAG = INT_INFO_DICT["configuration"][0]["interfaces"][0]["interface"][0]["apply-groups"][0]["data"]
        status_code=200

        if "hadoop" in VLAN_TAG.lower():
            VLAN_TAG = "Hadoop"
            #print(VLAN_TAG)
        elif "hyp" in VLAN_TAG.lower():
            VLAN_TAG = "Hypervisor"
            #print(VLAN_TAG)
        elif "ads" in VLAN_TAG.lower():
            VLAN_TAG = "Adserver"
            #print(VLAN_TAG)
        elif "dbser" in VLAN_TAG.lower():
            VLAN_TAG = "Database(DB)"
            #print(VLAN_TAG)
        elif "dev" in VLAN_TAG.lower():
            VLAN_TAG = "Development"
            #print(VLAN_TAG)
        else:
            VLAN_TAG
            #print(VLAN_TAG)


        return VLAN_TAG,status_code

    except Exception as e:
        print("ERROR:{0}".format(e))
        VLAN_TAG="null"
        DESC="null"
        status_code=404
        return VLAN_TAG,DESC,status_code