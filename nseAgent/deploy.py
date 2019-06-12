#!/usr/bin/python
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

nmapAgent = '''service nmapAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/nmapAgent.py -u
        port            = 25798
}
''' % cwd

nmapService = 'nseAgent       25798/tcp                       # nseAgent'


open('/etc/xinetd.d/nseAgent','w').write(nmapAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(nmapService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')