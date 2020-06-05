#!/opt/python/bin/python3
import smtplib
import csv
from email.message import EmailMessage
import sys

username = sys.argv[2]
password = sys.argv[3]
email = sys.argv[1]

def send_vpn_email(usermail, name, password):
    emailfrom = "DC-Network-Ops@pubmatic.com"
    emailto = usermail
    msg= EmailMessage()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Bcc"] = "santanu.mandal@pubmatic.com, tejas.mokashi@pubmatic.com, pravin.rathod@pubmatic.com"
    msg["Subject"] = ("VPN credential for SG3 DC")
    text = ("""
Hello,

Please find your VPN credential for SG3 DC.

 Username:  {0}
 Password:  {1}

 --SG3
 https://103.231.98.20:10443


## VPN Client Configuration:
Option1: Browser Based VPN
Windows & Mac system: Download plugin and connect for tunnel mode IPsec VPN.

Option2: VPN Client App based SSL VPN
Windows and mac system also can download and configure forticlient. Link to download Client: www.fortinet.com/support-and-training/support/product-downloads.html
Linux: Needs to download ssl vpn client and configure. [https://inside.pubmatic.com:8443/confluence/display/CC/VPN+client+configuration]

Option3: VPN Client App based IPsec VPN
Configure Forticlient/Native/3rd-party IPsec-VPN client.
Please attachement "VPN client configuration for Fortinet VPN-IPsec.docx" in confluence page [https://inside.pubmatic.com:8443/confluence/display/CC/VPN+client+configuration]


Thanks & Regards,
DC-Network-Ops
PubMatic
+91-Phone Number

    """.format(name, password))

    msg.set_content(text)
    try:
        server = smtplib.SMTP("My_organization.protection.outlook.com")
        server.send_message(msg)
        print("Sent mail to user {0}".format(usermail))

    except Exception as e:
        print("Error on sending email to user {0}".format(usermail))

def main():
   
   send_vpn_email(email, username, password)
   #send_vpn_email("tejas.mokashi@pubmatic.com", "tejas.mokashi", "xyz123")

if __name__ == '__main__':
    main()
