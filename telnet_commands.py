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
#switches = '''172.20.96.9
#172.20.96.10'''
switch_list = []
#switch_list = switches.split('\n')
command_list = command_text.split('\n')
def telnet_commands():
    for switch in switch_list:
        telnet = telnetlib.Telnet(switch)
        telnet.read_until(b'User Name')
        telnet.write(b'ztbot\n')
        telnet.read_until(b'Password')
        telnet.write(b'greenpointbot\n')
        telnet.read_until(b'#')
#telnet.write(b'conf\r\nvlan database\r\nvlan 111\r\nend\r\ncopy run start\r\ny')
#telnet.write(to_bytes(commands))
        for command in command_list:
            telnet.write(to_bytes(command))
        telnet.close()
        #time.sleep(0.5)


#telnet.read_until(b'maks_sw#')
#time.sleep(0.5)
#all_result = telnet.read_very_eager().decode('utf-8')
#print(all_result)
#with open('filename.txt', 'w') as f:
#    print(all_result, file=f)

with open('switches.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        switch_list.append(line)
#f.close()

telnet_commands()
print(datetime.now() - start_time)