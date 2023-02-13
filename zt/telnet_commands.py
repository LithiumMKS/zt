import telnetlib
import time
from datetime import datetime
import socket
import requests

start_time = datetime.now()  # обозначает время начала выполнения программы
url = 'http://ufa.groupw.ru/plugins/switch/config/5/switch.cfg'
r = requests.get(url, allow_redirects=True)
open('gw_switch.cfg', 'wb').write(r.content)  # запись в файл списка оборудования из гв

switch_dict = {}
with open('gw_switch.cfg', encoding="utf8") as f:  # Создание словаря, ключ - модель, значение - список айпишников
    for line in f:
        if 'alias' in line:
            switch_model = line.strip()[8:]
        elif 'address' in line:
            switch_ip = line.split()[-1]
            switch_dict.setdefault(switch_model, []).append(switch_ip)


def to_bytes(
        line):  # добавляет в строку знаки переноса и возврата каретки и преобразует в байтовое значение для чтения telnetlib
    return f"{line}\r\n".encode("utf-8")


def alc6224_login():
    alc6224_cfg = ''' 
    copy run start
    y
    '''
    telnet.read_until(b'User Name', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.read_until(b'Password', timeout=10)
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = alc6224_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command))


def des3526_login():
    des3526_cfg = '''
    config lldp ports 25-26 mgt_addr ipv4 {} enable
    save
    '''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = des3526_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))


def des3200_26_login():
    des3200_26_cfg = '''
    config lldp ports 25-26 mgt_addr ipv4 {} enable
    save
    '''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = des3200_26_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))

def des3200_52_login():
    des3200_52_cfg = '''
    create snmp community ZT_rw view CommunityView read_write
    save
    '''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = des3200_52_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))

def des1210_28_login():
    des1210_28_cfg = '''delete snmp group ZT_rw
delete snmp community ZT_rw
create snmp group ZT_rw v1 read_view ReadWrite write_view ReadWrite notify_view ReadWrite
create snmp group ZT_rw v2c read_view ReadWrite write_view ReadWrite notify_view ReadWrite
create snmp community ZT_rw view ReadWrite read_write
save
'''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName:', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.read_until(b'Password:', timeout=10)
    telnet.write(b'greenpointbot\n')

    telnet.read_until(b'#', timeout=10)

    command_list = des1210_28_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))
        telnet.read_until(b'#')



def dgs3627_login():
    dgs3627_cfg = '''
config ddm power_unit dbm
save

    '''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = dgs3627_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))


def dgs3620_login():
    dgs3620_cfg = '''
    config ddm power_unit dbm
    save

    '''
    telnet = telnetlib.Telnet(switch, timeout=20)
    telnet.set_debuglevel(3)
    telnet.read_until(b'UserName', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'#', timeout=10)
    command_list = dgs3620_cfg.split('\n')
    for command in command_list:
        telnet.write(to_bytes(command.format(switch)))

def alc6850_login():
    alc6850_cfg = '''
interfaces transceiver ddm enable 
    '''
    telnet.read_until(b'login : ', timeout=10)
    telnet.write(b'ztbot\n')
    telnet.read_until(b'password : ', timeout=10)
    telnet.write(b'greenpointbot\n')
    telnet.read_until(b'# ', timeout=10)
    command_list = alc6850_cfg.split('\n')
#    for command in command_list:
#       telnet.write(to_bytes(command))
    telnet.write(b'interfaces transceiver ddm enable\n')
    telnet.read_until(b'# ', timeout=10)

def telnet_commands(model):
    switch_list = switch_dict.get(model)
    global switch  # Для использования в функциях
    for switch in switch_list:
        try:
            global telnet  # для использования в других функциях
            telnet = telnetlib.Telnet(switch, timeout=20)
            telnet.set_debuglevel(3)
            if model == 'OS-LS-6224':
                alc6224_login()
            if model == 'DES-3526':
                des3526_login()
            if model == 'DES-3200-26':
                des3200_26_login()
            if model == 'DES-3200-52/C1 Fast Ethernet Switch':
                des3200_52_login()
            if model == 'DES-1210-28/ME/B2':
                des1210_28_login()
            if model == 'DGS-3627G':
                dgs3627_login()
            if model == 'DGS-3620-28SC':
                dgs3620_login()
            if model == 'OS-6850-U24X':
                alc6850_login()
        except socket.timeout:  # позволяет продолжить выполнение, если хост не отвечает по таймауту
            print("connection time out caught")



# with open('switches.txt', 'r') as f: ##считывает ip из файла и заполняет ими список switch_list
#    switch_list = []  ##пустой список коммутаторов, который в дальнейшем будет заполняться и обрабатываться
#    lines = f.readlines()
#    for line in lines:
#        line = line.strip()
#        switch_list.append(line)

telnet_commands('DES-3200-52/C1 Fast Ethernet Switch')
# telnet_commands('OS-LS-6224')
print(datetime.now() - start_time)  # считает время выполнения программы
