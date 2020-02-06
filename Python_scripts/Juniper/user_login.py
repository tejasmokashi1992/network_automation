#!/opt/python/bin/python3

from netmiko import ConnectHandler
from getpass import getpass
from threading import Thread
import json
#username = input('Enter your SSH username: ')
password = getpass()

class NetworkAudit(Thread):
    def __init__(self,device):
        Thread.__init__(self)
        self.device = device

    def run(self):
        print("Running Audit on "+self.device)
        audit(self.device)


def audit(device):
        ip_address_of_device = device
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': 'tejas.mokashi',
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            result = net_connect.send_command('show configuration system login | display json')
            with open( 'user_audit.json', 'w' ) as user_audit:
                user_audit.write(result+"\n")
            with open('user_audit.json', 'r' ) as f:
                out_json = f.read()
            #print(out_json)
            json_dict = json.loads(out_json)
            #print(json_dict)
            for i in range(0, 10):
               user = (json_dict["configuration"]["system"]["login"]["user"][0+i]["name"])
               commands_list=["delete system login user {0}".format(user), "commit"]
               if user == "ben.villatore" or user == "santanu.mandal" or user == "tejas.mokashi" or user == "pravin.rathod":
                   pass
               else:
                   try:
                      print(user)
                      show_compare = net_connect.send_config_set("show | compare")
                      if "The configuration has been changed but not committed" not in show_compare:
                         output = net_connect.send_config_set(commands_list, delay_factor=3)
                         time.sleep(30)
                         print(output)
                         if "configuration check succeeds" in output or "Exiting configuration mode" in output:
                             print("!!!!!!!!!!!!!Configuration Successful.!!!!!!!!!!!!!")
                         else:
                             print("!!!!!!!!!!!!!Configuration Failed.!!!!!!!!!!!!!")
                      else:
                          print("Config already on candidate page. Need to check manually")
                          net_connect.disconnect()
                   except Exception as e:
                      print("ERROR:{0}".format(e))

        except Exception as e:
            print("ERROR:{0}".format(e))


def main():
    with open('devices_file') as f:
        device_list = f.read().splitlines()
        print(device_list)

    thread_list=[]
    for device in device_list:
        audit=NetworkAudit(device)
        thread_list.append(audit)
        audit.start()
    for thread in thread_list:
        thread.join()

    print("=====================================")
    print("Done checking all devices")
    print("=====================================")

if __name__ == '__main__':
    main()
