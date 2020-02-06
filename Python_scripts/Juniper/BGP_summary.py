#!/opt/python/bin/python3

from netmiko import ConnectHandler
#from getpass import getpass
import json
from bgp_email_script import send_peer_down_email
import time
#username = input('Enter your SSH username: ')
#password = getpass()
localtime = time.asctime( time.localtime(time.time()) )
print ("Local current time :", localtime)

def audit(device):
        ip_address_of_device = device
        junos_device = {
            'device_type': 'juniper',
            'ip': ip_address_of_device,
            'username': 'net.ops',
            'password': 'NetOps@321'
        }
        try:
            net_connect = ConnectHandler(**junos_device)
            output = net_connect.send_command('show bgp summary | display json | no-more')
            with open( 'bgp_output.json', 'w' ) as bgp_output:
                bgp_output.write(output+"\n")
            net_connect.disconnect()
            with open('bgp_output.json', 'r' ) as f:
                out_json = f.read()
            #print(out_json)
            json_dict = json.loads(out_json)
            #print(json_dict)

            BGP_Peer_count = int(json_dict["bgp-information"][0]["peer-count"][0]["data"])
            for i in range(0, BGP_Peer_count):
               BGP_Peer_AS = json_dict["bgp-information"][0]["bgp-peer"][0+i]["peer-as"][0]["data"]                       
            
               if BGP_Peer_AS == "3356" or BGP_Peer_AS == "3257":
                  BGP_Nei_IP = json_dict["bgp-information"][0]["bgp-peer"][0+i]["peer-address"][0]["data"]
                  BGP_State = json_dict["bgp-information"][0]["bgp-peer"][0+i]["peer-state"][0]["data"]
                  BGP_Time_Sec = int(json_dict["bgp-information"][0]["bgp-peer"][0+i]["elapsed-time"][0]["attributes"]["junos:seconds"])
                  BGP_Desc = json_dict["bgp-information"][0]["bgp-peer"][0+i]["description"][0]["data"]
                  Peer_info = list(BGP_Desc.split())
                  BGP_MailID = Peer_info[3]
                  BGP_CircuitID = Peer_info[1]
                  BGP_Name = Peer_info[0]
                  print(BGP_Nei_IP)
                  print(BGP_State)
                  print(BGP_MailID)
                  print(BGP_CircuitID)

                  if (BGP_State != "Established") and (300 < BGP_Time_Sec < 2100):
                     print("sending mail")
                     send_peer_down_email(BGP_MailID, BGP_Nei_IP, BGP_CircuitID, BGP_Name)
                  else:
                     print("All OK")                    
                  
        except Exception as e:
            print("ERROR:{0}".format(e))


def main():
    with open('core_routers') as f:
        device_list = f.read().splitlines()
        #print(device_list)
    for device in device_list:    
        audit(device)


    print("=====================================")
    print("Done checking all devices")
    print("=====================================")

if __name__ == '__main__':
    main()

