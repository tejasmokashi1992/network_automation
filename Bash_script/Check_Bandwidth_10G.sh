#!/bin/bash
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

SNMP_SECRET='75Pubm4t1cSNMP'
IP=$1
IN_OID=$2
OUT_OID=$3

IN=$(snmpget -v2c -c $SNMP_SECRET -OQv $IP $IN_OID)
OUT=$(snmpget -v2c -c $SNMP_SECRET -OQv $IP $OUT_OID)
PIPE=8000000000
INMB=$(((IN)/1000000))
OUTMB=$(((OUT)/1000000))
TOTALBW=10000000000
#PRCNTIN=$((($IN/$TOTALBW)*100))
#PRCNTOUT=$((($OUT/$TOTALBW)*100))
PRCNTIN=$(((IN*100)/$TOTALBW))
PRCNTOUT=$(((OUT*100)/$TOTALBW))


        if [ -z "$OUT" ] || [ -z "$IN" ]; then
                msg="Unable to retrieve SNMP info."
                state=CRITICAL
                echo $state $msg
                exit $STATE_CRITICAL

        else


                  if [ $IN -gt $PIPE ]|| [ $OUT -gt $PIPE ]
                  then
                    msg="Inbound: $INMB "Mbps" ($PRCNTIN% Used), Outbound: $OUTMB "Mbps" ($PRCNTOUT% Used) | 'in'= $INMB ,'out'= $OUTMB"
                    state=CRITICAL
                    echo $state $msg
                    exit $STATE_CRITICAL
                  else
                    msg="Inbound: $INMB "Mbps" ($PRCNTIN% Used), Outbound: $OUTMB "Mbps" ($PRCNTOUT% Used) | 'in'= $INMB ,'out'= $OUTMB"
                    state=OK
                    echo $state $msg
                    exit $STATE_OK
                  fi
        fi
       
