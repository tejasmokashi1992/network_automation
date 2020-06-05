#!/opt/python/bin/python3

from passgen import password_gen
import os

USER_FILE='/usr/local/src/PLAYBOOKS/scripts/userlist'
OUTPUT_FILE='/usr/local/src/PLAYBOOKS/scripts/output.txt'
p=password_gen()

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

with open(USER_FILE,'r') as f:
    for line in f.readlines():
        with open(OUTPUT_FILE,'a') as f1:
            user_name = line.strip()
            password = p.passgen(str(user_name))
            email_id = user_name+'@pubmatic.com'
            str_to_write=email_id+","+user_name+","+password
            f1.write(str_to_write+"\n")

#line_prepender(OUTPUT_FILE,"email_id,username,password")
