#!/bin/bash
STATE_OK=0
STATE_CRITICAL=2
MPLS_IN=`snmpget -v2c -c 75Pubm4t1cSNMP -OQv 10.161.2.4 1.3.6.1.4.1.2636.3.3.1.1.7.778`
MPLS_OUT=`snmpget -v2c -c 75Pubm4t1cSNMP -OQv 10.161.2.4  1.3.6.1.4.1.2636.3.3.1.1.8.778`
MPLS_IN_MBIT=`echo "$MPLS_IN/10^6" | bc`
MPLS_OUT_MBIT=`echo "$MPLS_OUT/10^6" | bc`
MPLS_IN_1=`snmpget -v2c -c 75Pubm4t1cSNMP -OQv 10.161.2.5 1.3.6.1.4.1.2636.3.3.1.1.7.1148`
MPLS_OUT_1=`snmpget -v2c -c 75Pubm4t1cSNMP -OQv 10.161.2.5  1.3.6.1.4.1.2636.3.3.1.1.8.1148`
MPLS_IN_MBIT_1=`echo "$MPLS_IN_1/10^6" | bc`
MPLS_OUT_MBIT_1=`echo "$MPLS_OUT_1/10^6" | bc`
MPLS_IN_MBIT=`echo "$MPLS_IN_MBIT+$MPLS_IN_MBIT_1"|bc`
MPLS_OUT_MBIT=`echo "$MPLS_OUT_MBIT+$MPLS_OUT_MBIT_1"|bc`
msg= "Inbound: $MPLS_IN_MBIT "Mbps" , Outbound: $MPLS_OUT_MBIT "Mbps"  | 'in'= $MPLS_IN_MBIT ,'out'= $MPLS_OUT_MBIT"
echo $msg
exit $STATE_OK