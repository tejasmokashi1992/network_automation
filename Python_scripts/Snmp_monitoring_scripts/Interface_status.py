
#!/opt/python/bin/python3
# Module for getting arguments/inputs from user.
import argparse
# Used here for exiting script with status code.
import sys
# Module for sending commands to bash shell.    
import subprocess

STATE_OK=0
STATE_CRITICAL=2

def get_status(IP, OID):
    try:
        SNMP_SECRET='SNMPstring'
        # command to get required data from device.
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(OID)
        # Run above command on bash shell with subprocess.
        STATUS=(subprocess.getoutput(command))
        
        # if STATUS is empty the print unable to retrive snmp info.
        if not STATUS:
            MSG="Unable to retrieve SNMP info."
            print("CRITICAL:{0}".format(MSG))
            sys.exit(2)
        else:
            # if interfaces is up exit script with status code 0 ie OK.
            if STATUS == 'up':
                MSG="Interface is Up"
                print("OK: {0}".format(MSG))
                sys.exit(0)
            else:
            # if interfaces is down exit script with status code 2 ie CRITICAL.
                MSG="Interface is Down"
                print("CRITICAL: {0}".format(MSG))
                sys.exit(2)
    except Exception as e:
            print("ERROR:{0}".format(e))
            sys.exit(2)

def main():
    # create a object from argparse.
    parser = argparse.ArgumentParser()
    # make a input option to accept IP address.
    parser.add_argument('--ip')
    # make a input option to accept SNMP OID.
    parser.add_argument('--oid')
    args = parser.parse_args()
    ip=args.ip
    oid=args.oid
    # call our get_status function defined above.
    get_status(ip, oid)

if __name__ == '__main__':
    main()


Usage:
================================
command[check_TS1-to-OOB_Equinix_Connect]=/usr/lib64/nagios/plugins/pub/interface_status.py --ip 10.91.2.70 --oid .1.3.6.1.2.1.2.2.1.8.3
