#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

niktoAgent = '''service niktoAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/niktoAgent.py -u
        port            = 25801
}
''' % cwd

nitkoService = 'niktoAgent       25801/tcp                       # niktoAgent\n'


open('/etc/xinetd.d/niktoAgent','w').write(niktoAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(nitkoService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

# create Log Path
path = "/var/log/nikto"
os.mkdir(path)

print ("Log Path is created")

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')