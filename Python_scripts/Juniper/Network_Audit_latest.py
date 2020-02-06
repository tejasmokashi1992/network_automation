#!/opt/python/bin/python3

#ConnectHandler factory function selects the correct Netmiko class based upon the device_type
from netmiko import ConnectHandler
#Prompt the user for a password without echoing.
from getpass import getpass
from threading import Thread

username = input('Enter your SSH username: ')
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
            'username': username,
            'password': password
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            output = net_connect.send_command('show configuration | display set | match syslog | match host')

            if "10.161.2.126" not in output:

                print("Configuration not found on :{0}".format(device))
                with open( 'unconfigured_devices', 'a+' ) as audit_out:
                    audit_out.write(device+"\n")
 #                   audit_out.write( output )
                net_connect.disconnect()  
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
