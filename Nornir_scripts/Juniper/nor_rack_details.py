#!/usr/bin/python3
import json
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import re
from flask import (Flask,request,send_file,jsonify,abort,Response,url_for)
from flask import make_response
from waitress import serve

nr = InitNornir(
    inventory={
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
            "defaults_file": "inventory/defaults.yaml",
        }
    }
)
app = Flask(__name__)

#@app.route("/vlantag", methods=['GET'])
def check_tag():
    RACK_NUM = request.args.get('rack_num')
    RU_NUM = request.args.get('ru_num')
    #print(RACK_NUM)
    #print(RU_NUM)
    try:
        HOST = "TOR_"+ (RACK_NUM)
        #print(HOST)
        TOR_IP = nr.inventory.hosts[HOST].hostname
        #print(TOR_IP)
        SWITCH = nr.filter(F(hostname=TOR_IP))
        RU_CONF = SWITCH.run(task=netmiko_send_command, command_string="show configuration | display set | match RU{0}".format(RU_NUM))
        print(RU_CONF)
        CONF_LIST = RU_CONF[HOST].result.split()
        print(CONF_LIST)
        subs = 'ae'
        # using re + search()
        # to get string with substring
        RES = [x for x in CONF_LIST if re.search(subs, x)]
        #print(RES)
        SERVER_INTERFACE = RES[0]
        #print(SERVER_INTERFACE)

        INT_INFO = SWITCH.run(task=netmiko_send_command, command_string="show configuration interfaces {0} | display json | no-more".format(SERVER_INTERFACE))
        INT_INFO_DICT = json.loads(INT_INFO[HOST].result)
        VLAN_TAG = INT_INFO_DICT["configuration"][0]["interfaces"][0]["interface"][0]["apply-groups"][0]["data"]
        DESC = INT_INFO_DICT["configuration"][0]["interfaces"][0]["interface"][0]["description"][0]["data"]
        status_code=200

        if "hadoop" in VLAN_TAG.lower():
            VLAN_TAG = "Hadoop"
            print(VLAN_TAG)
        elif "hyp" in VLAN_TAG.lower():
            VLAN_TAG = "Hypervisor"
            print(VLAN_TAG)
        elif "ads" in VLAN_TAG.lower():
            VLAN_TAG = "Adserver"
            print(VLAN_TAG)
        elif "dbser" in VLAN_TAG.lower():
            VLAN_TAG = "Database(DB)"
            print(VLAN_TAG)
        elif "dev" in VLAN_TAG.lower():
            VLAN_TAG = "Development"
            print(VLAN_TAG)
        else:
            VLAN_TAG
            print(VLAN_TAG)


        return VLAN_TAG,DESC,status_code

    except Exception as e:
        print("ERROR:{0}".format(e))
        VLAN_TAG="null"
        DESC="null"
        status_code=404
        return VLAN_TAG,DESC,status_code

@app.route('/vlantag/', methods=['GET'])
def to_json():

    VLAN_TAG,DESC,status_code=check_tag()
    return (jsonify({"SERVER_INFO":{"VLAN_TAG":VLAN_TAG,
        "RACK_UNIT_NUMBER":DESC}}),status_code)
    #return ("""SERVER VLAN_TAG: {0} \n SERVER RU_NUM: {1}""".format(VLAN_TAG,DESC))
    #return status_code

if __name__ == '__main__':
    #app.run(debug=True,host="192.168.0.31",port=9092)
    serve(app, host='192.168.137.1', port=9092)