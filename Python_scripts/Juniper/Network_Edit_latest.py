#!/opt/python/bin/python3

#ConnectHandler factory function selects the correct Netmiko class based upon the device_type
from netmiko import ConnectHandler
#Prompt the user for a password without echoing.
from getpass import getpass
from threading import Thread
import time
username = input('Enter your SSH username: ')
password = getpass()

commands_list=['set system archival configuration transfer-on-commit', 'set system archival configuration archive-sites "scp://copy@10.191.2.125:/opt/config_backup" password "AvrY9CBvUnid61jc"','yes', 'commit']

class NetworkEdit(Thread):
    def __init__(self,device):
        Thread.__init__(self)
        self.device = device

    def run(self):
        print("Running Edit on "+self.device)
        edit(self.device)


def edit(device):
        ip_address_of_device = device
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': username,
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            show_compare = net_connect.send_config_set("show | compare")
            #print(show_compare)
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

def main():
    with open('devices_file') as f:
        device_list = f.read().splitlines()
        print(device_list)

        thread_list=[]
        for device in device_list:
            edit=NetworkEdit(device)
            thread_list.append(edit)
            edit.start()
        for thread in thread_list:
            thread.join()

    print("=====================================")
    print("Done configuring all devices")
    print("=====================================")

if __name__ == '__main__':
    main()
