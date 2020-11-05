#!/opt/python/bin/python3
import argparse
import sys
import subprocess

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2


def get_BW(IP, IN_OID, OUT_OID, SPEED):
    try:
        SNMP_SECRET='75Pubm4t1cSNMP'
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(IN_OID)
        IN=int(subprocess.getoutput(command))
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(OUT_OID)
        OUT=int(subprocess.getoutput(command))
        INMB=int((IN)/1000000)
        OUTMB=int((OUT)/1000000)
        command="snmpget -v2c -c "+str(SNMP_SECRET)+" -OQv "+str(IP)+"  "+str(SPEED)
        TOTALBW=int(subprocess.getoutput(command))
        CAPACITY=int(TOTALBW/1000)
        WARNING_BW=int(0.75*TOTALBW)
        CRITICAL_BW=int(0.85*TOTALBW)
        PRCNTIN= int((INMB*100)/TOTALBW)
        PRCNTOUT= int((OUTMB*100)/TOTALBW)


        if INMB >= CRITICAL_BW or OUTMB >= CRITICAL_BW:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps | 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("CRITICAL {0}".format(MSG))
             sys.exit(2)
        elif INMB >= WARNING_BW or OUTMB >= WARNING_BW:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps| 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("WARNING {0}".format(MSG))
             sys.exit(1)
        else:
             MSG=("Inbound:{0} Mbps ({2}% used), Outbound:{1} Mbps ({3}% used), Capacity:{4} Gbps | 'in'= {0}, 'out'= {1}".format(INMB,OUTMB,PRCNTIN,PRCNTOUT,CAPACITY))
             print("OK {0}".format(MSG))
             sys.exit(0)
    except Exception as e:
             print("ERROR:{0}".format(e))
             sys.exit(2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--in_oid')
    parser.add_argument('--out_oid')
    parser.add_argument('--speed')
    args = parser.parse_args()
    ip=args.ip
    in_oid=args.in_oid
    out_oid=args.out_oid
    speed=args.speed
    get_BW(ip, in_oid, out_oid, speed)


if __name__ == '__main__':
    main()


Usage:
=======================
command[check_bw_gtt]=/usr/lib64/nagios/plugins/pub/check_bandwidth.py --ip 10.111.2.50 --in_oid .1.3.6.1.4.1.2636.3.3.1.1.7.556 --out_oid .1.3.6.1.4.1.2636.3.3.1.1.8.556 --speed 1.3.6.1.2.1.31.1.1.1.15.556
command[check_bw_Level3]=/usr/lib64/nagios/plugins/pub/check_bandwidth.py --ip 10.111.2.51 --in_oid .1.3.6.1.4.1.2636.3.3.1.1.7.558 --out_oid .1.3.6.1.4.1.2636.3.3.1.1.8.558 --speed 1.3.6.1.2.1.31.1.1.1.15.558
