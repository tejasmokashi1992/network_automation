#!/opt/python/bin/python3
import argparse
import sys
import subprocess

STATE_OK=0
STATE_CRITICAL=2

def get_status(IP, OID):
    try:
        SNMP_SECRET='75Pubm4t1cSNMP'
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(OID)
        STATUS=(subprocess.getoutput(command))

        if not STATUS:
            MSG="Unable to retrieve SNMP info."
            print("CRITICAL:{0}".format(MSG))
            sys.exit(2)
        else:
            if STATUS == 'up':
                MSG="Interface is Up"
                print("OK: {0}".format(MSG))
                sys.exit(0)
            else:
                MSG="Interface is Down"
                print("CRITICAL: {0}".format(MSG))
                sys.exit(2)
    except Exception as e:
            print("ERROR:{0}".format(e))
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--oid')
    args = parser.parse_args()
    ip=args.ip
    oid=args.oid
    get_status(ip, oid)

if __name__ == '__main__':
    main()
