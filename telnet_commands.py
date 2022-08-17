import telnetlib
import time
from datetime import datetime
start_time = datetime.now()

def to_bytes(line):
    return f"{line}\r\n".encode("utf-8")

command_text = '''
copy run start
y
'''

switch_list = []
command_list = command_text.split('\n')
def telnet_commands():
    for switch in switch_list:
        telnet = telnetlib.Telnet(switch)
        telnet.read_until(b'User Name')
        telnet.write(b'ztbot\n')
        telnet.read_until(b'Password')
        telnet.write(b'greenpointbot\n')
        telnet.read_until(b'#')
        for command in command_list:
            telnet.write(to_bytes(command))
        telnet.close()

with open('switches.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        switch_list.append(line)

telnet_commands()
print(datetime.now() - start_time)