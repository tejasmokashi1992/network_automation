import smtplib
from email.message import EmailMessage

def send_peer_down_email(BGP_MailID, BGP_Nei_IP, BGP_CircuitID, BGP_Name):
    emailfrom = "DC-Network-Ops@pubmatic.com"
    emailto = BGP_MailID
    msg= EmailMessage()
    msg["From"] = emailfrom
    msg["To"] =emailto
    msg["Subject"] = ("Observing BGP peering to be down with {0}".format(BGP_Name))
    text= 
    (""" 
    Hello NOC,
    
    We are observing that our BGP Neighborship is down with you.
    Kindly check on priority.

    Your end IP: {0}
    Pubmatic AS number: 62713
    {1}

    Thanks & Regards,
    DC-Network-Ops
    PubMatic 
    +19162778659

    """.format(BGP_Nei_IP, BGP_CircuitID))

    msg.set_content(text)
    try:
        server = smtplib.SMTP("pubmatic-com.mail.protection.outlook.com")
        server.send_message(msg)
        
    except Exception as e:
        print("Error on sending email")