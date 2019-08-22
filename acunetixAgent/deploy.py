#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

acunetixAgent = '''service acunetixAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/acunetixAgent.py -u
        port            = 25700
}
''' % cwd

acunetixService = 'acunetixAgent       25700/tcp                       # acunetixAgent\n'


open('/etc/xinetd.d/acunetixAgent','w').write(acunetixAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(acunetixService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')