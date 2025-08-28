#!/opt/python/bin/python3
# Module for getting arguments/inputs from user.
import argparse
# Used here for exiting script with status code.
import sys
# Module for sending commands to bash shell.    
import subprocess

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2


def get_BW(IP, IN_OID, OUT_OID, SPEED):
    try:
        SNMP_SECRET='SNMPstring'
        # command to get required data from device.
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(IN_OID)
         # Run above command on bash shell with subprocess & store output in IN variable.
        IN=int(subprocess.getoutput(command))
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(OUT_OID)
        OUT=int(subprocess.getoutput(command))
        # convert the input & output bandwidth data to MBps for readability & processing.
        INMB=int((IN)/1000000)
        OUTMB=int((OUT)/1000000)
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(SPEED)
        TOTALBW=int(subprocess.getoutput(command))
        # calculate the total capacity of link.
        CAPACITY=int(TOTALBW/1000)
        # define warning bandwidth to 75%
        WARNING_BW=int(0.75*TOTALBW)
        # define critical bandwidth to 85%
        CRITICAL_BW=int(0.85*TOTALBW)
        PRCNTIN= int((INMB*100)/TOTALBW)
        PRCNTOUT= int((OUTMB*100)/TOTALBW)

        # if input or output traffic on link is above 85% then give critical alert.
        if INMB >= CRITICAL_BW or OUTMB >= CRITICAL_BW:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps | 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("CRITICAL {0}".format(MSG))
             sys.exit(2)
        # if input or output traffic on link is above 75% then give warning alert.
        elif INMB >= WARNING_BW or OUTMB >= WARNING_BW:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps| 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("WARNING {0}".format(MSG))
             sys.exit(1)
        # if input or output traffic on link is below 75% then give OK message.
        else:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps | 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("OK {0}".format(MSG))
             sys.exit(0)
    # if there is any expection the print that exception & exit with status code 2.
    except Exception as e:
             print("ERROR:{0}".format(e))
             sys.exit(2)

def main():
    # create a object from argparse
    parser = argparse.ArgumentParser()
    # make a input option to accept IP address.
    parser.add_argument('--ip')
    # make a input option to accept SNMP OID for getting input bandwidth.
    parser.add_argument('--in_oid')
    # make a input option to accept SNMP OID for getting output bandwidth.
    parser.add_argument('--out_oid')
    # make a input option to accept SNMP OID for getting speed of link/interface.
    parser.add_argument('--speed')
    args = parser.parse_args()
    ip=args.ip
    in_oid=args.in_oid
    out_oid=args.out_oid
    speed=args.speed
    # call our get_BW function defined above.
    get_BW(ip, in_oid, out_oid, speed)


if __name__ == '__main__':
    main()


Usage:
=======================
command[check_bw_gtt]=/usr/lib64/nagios/plugins/pub/check_bandwidth.py --ip 10.111.2.50 --in_oid .1.3.6.1.4.1.2636.3.3.1.1.7.556 --out_oid .1.3.6.1.4.1.2636.3.3.1.1.8.556 --speed 1.3.6.1.2.1.31.1.1.1.15.556
command[check_bw_Level3]=/usr/lib64/nagios/plugins/pub/check_bandwidth.py --ip 10.111.2.51 --in_oid .1.3.6.1.4.1.2636.3.3.1.1.7.558 --out_oid .1.3.6.1.4.1.2636.3.3.1.1.8.558 --speed 1.3.6.1.2.1.31.1.1.1.15.558
