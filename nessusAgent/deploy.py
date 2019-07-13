#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

nessusAgent = '''service nessusAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/nessusAgent.py -u
        port            = 25701
}
''' % cwd

nessusService = 'nessusAgent       25701/tcp                       # nessusAgent\n'


open('/etc/xinetd.d/nessusAgent','w').write(nessusAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(nessusService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')