import telnetlib
import time
from datetime import datetime

start_time = datetime.now() ##обозначает время начала выполнения программы
command_text = ''' 
conf
spanning-tree pathcost method long
end
copy run start
y
'''

switch_list = [] ##пустой список коммутаторов, который в дальнейшем будет заполняться и обрабатываться
command_list = command_text.split('\n') ##список команд, составленный путем разделения текста на строки

def to_bytes(line): ##добавляет в строку знаки переноса и возврата каретки и преобразует в байтовое значение для чтения telnetlib
    return f"{line}\r\n".encode("utf-8")

def telnet_commands():
    for switch in switch_list:
        telnet = telnetlib.Telnet(switch, timeout=1)
        telnet.read_until(b'User Name')
        telnet.write(b'ztbot\n')
        telnet.read_until(b'Password')
        telnet.write(b'greenpointbot\n')
        telnet.read_until(b'#')
        for command in command_list:
            telnet.write(to_bytes(command))
        telnet.close()

with open('switches.txt', 'r') as f: ##считывает ip из файла и заполняет ими список switch_list
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        switch_list.append(line)

telnet_commands()
print(datetime.now() - start_time) ##считает время выполнения программы