#!/opt/python/bin/python3
from easysnmp import Session
from collections import Counter
import time
import os
import ftplib
import paramiko

DC='NJR3'
TIME=time.strftime('%Y-%m-%d_%H:%M:%S')
BASE_PATH="/var/tmp/"
FILE_NAME=BASE_PATH+DC+"_"+TIME
session = Session(hostname='10.191.2.9', community='75Pubm4t1cSNMP', version=2)
system_items = session.walk('1.3.6.1.4.1.12356.101.11.2.1.1.3')
IP_LIST=[]

if len(system_items) > 0:
    IP_LIST=[system_items[i].value for i in range(0,len(system_items))]


SOURCE_LIST=Counter(IP_LIST).most_common(10)
#print(c.most_common(10))
with open(FILE_NAME,'w') as f:
    f.writelines("TOP 10 SOURCE IP LIST MAKING SESSION\n")
    f.writelines("IP\t\t\t\t\t\t\tSESSION\n")
    for i in range(0,len(SOURCE_LIST)):
        IP=SOURCE_LIST[i][0]
        SESSION=SOURCE_LIST[i][1]
        f.writelines("{0}\t\t\t\t\t\t\t{1}\n".format(IP,SESSION))


system_items = session.walk('1.3.6.1.4.1.12356.101.11.2.1.1.5')
IP_LIST=[]

if len(system_items) > 0:
    IP_LIST=[system_items[i].value for i in range(0,len(system_items))]

DESTINATION_LIST=Counter(IP_LIST).most_common(10)
with open(FILE_NAME,'a') as f:
    f.writelines("\nTOP 10 DESTINATION IP LIST MAKING SESSION\n")
    f.writelines("IP\t\t\t\t\t\t\tSESSION\n")
    for i in range(0,len(SOURCE_LIST)):
        IP=DESTINATION_LIST[i][0]
        SESSION=DESTINATION_LIST[i][1]
        f.writelines("{0}\t\t\t\t\t\t\t{1}\n".format(IP,SESSION))
    f.close()

try:
    if os.path.isfile(FILE_NAME):
        FTP_SERVER='10.160.131.25'
        BASE_FILE=FILE_NAME.split('/')[3]
        REMOTE_PATH="/home/copyuser/fortinet_session_monitor/"+BASE_FILE
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        ssh.connect(FTP_SERVER, username='copyuser', password='wrexa_H2')
        ftp = ssh.open_sftp()
        ftp.chdir("fortinet_session_monitor")
        ftp.put(FILE_NAME,REMOTE_PATH)
        ftp.close()
        ssh.close()
        print("File uploaded successfully to FTP server {0} PATH={1}".format(FTP_SERVER,REMOTE_PATH))
except ftplib.all_errors as e:
    print(e)
