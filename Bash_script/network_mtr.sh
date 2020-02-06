#!/bin/bash
IP=`ip r l|grep 'kernel'|awk '{print $9}' | grep '^10\b'`
DATE=`date +%Y_%m_%d_%H_%M_%S`
file="/var/tmp/${IP}_${DATE}.txt"
url=$1
check_packages()
{

    rpm  -qa |grep  traceroute
    if [ $? -ne 0 ]
    then

       yum install traceroute -y
        if [ $? -eq 0 ];
        then
        echo "installed traceroute successfully"
        fi
    fi

    rpm  -qa |grep  ftp
    if [ $? -ne 0 ]
    then
      version=`cat /etc/redhat-release|awk -F 'release' '{print $2}' | cut -d '.' -f1`
      if [ $version -eq 6 ]
      then

            wget ftp://copyuser:wrexa_H2@162.248.19.40/ftp-0.17-54.el6.x86_64.rpm
            rpm -ivh ftp-0.17-54.el6.x86_64.rpm
            echo "installed ftp client"
      elif [ $version -eq 7 ]
      then
             wget ftp://copyuser:wrexa_H2@162.248.19.40/ftp-0.17-67.el7.x86_64.rpm
             rpm -ivh ftp-0.17-67.el7.x86_64.rpm
             echo "installed ftp client"
      else
           echo "Found different OS version"
       fi
    fi

     rpm -qa|grep  net-tools
      if [ $? -ne 0 ]
      then
        yum install net-tools -y
           if [ $? -eq 0 ];
           then
          echo "installed net-tools successfully"
        fi
      fi

    check_mtr_version=`mtr --version|awk '{print $2}'`
    expect=0.85
   if (($(echo "$check_mtr_version < $expect" | bc)))
    then

            install_mtr
    fi
}


calculate()
{



   echo "Local file path:$file"
   url=$url
   echo "=========== NETWORK STATS for $url =====================" >> $file
   echo "IP ADDRESS[PUBLIC/PRIVATE]:`ip r l|grep 'kernel'|awk '{print $9}'|paste -sd' '` " >> $file
   echo "++++ route  ++++" >> $file
   route -n  >> $file
   echo "++++ Ping check ++++"  >> $file
   ping -c 100  $url  >> $file
   echo "===============================" >> $file
   echo "++++ Command 1: traceroute ++++"  >> $file
   traceroute $url >> $file
   echo "++++ Command 2: traceroute -n ++++" >> $file
   traceroute -n $url >> $file
   echo "++++ Command 3: traceroute -n -I ++++" >> $file
   traceroute -n -I $url >> $file
   echo "++++ Command 4: traceroute -T  ++++" >> $file
   traceroute -T $url >> $file
   echo "++++ Command 5: traceroute -T -p 80  ++++" >> $file
   traceroute -T -p 80 $url >> $file
   echo "========= MTR Report===========" >> $file
   echo "++++ Command 6: mtr –-report -c +++++" >> $file
   mtr --report -c 100 $url  >> $file
   echo "++++ Command 7: mtr –-report –tcp -p 80 +++++" >> $file
   mtr --report --tcp -P 80 -c 100 $url  >> $file
   echo "++++ Command 8: mtr –-report -n –tcp -p 80 -c 100  +++++" >> $file
   mtr --report -n --tcp -P 80 -c 100 $url   >> $file
   echo "=========================="
   mtr --report -n --tcp -P 80 -c 100 $url   >> $file
   echo "=========================="
   mtr --report -n --tcp -P 80 -c 100 $url   >> $file
   echo "=========================="
   echo "++++ Command 9: dig <URL> ++++ " >> $file
   dig $url >> $file
   echo "++++ Command 10: dig 8.8.8.8 ++++" >> $file
   dig  8.8.8.8 >> $file

#######Uploading to ftp
curl -T "${file}" ftp://copyuser:wrexa_H2@162.248.19.40/network-lat-files/
if [ $? -eq 0 ]
then
   echo "FIle $file uploaded to ftp server 162.248.19.40 successfully"
else
   echo "File upload failed"
fi

}

install_mtr()
{

check=`rpm -qa |grep mtr`
rpm -e $check
wget ftp://copyuser:wrexa_H2@162.248.19.40/mtr-0.85-4.gf.el6.x86_64.rpm
rpm -ivh  mtr-0.85-4.gf.el6.x86_64.rpm


version=`mtr --version|awk '{print $2}'`
if [ $version == "0.85" ]
then
   echo "installed mtr version 0.85 successfully "
else
   echo "falied to  install mtr version"
fi
}

main()
{

if [ "$url" == "" ]
then
    echo "Provide url to check"
    echo " e.g. network.sh <url>"
    exit 2
fi

check_packages
calculate $url
}
main
