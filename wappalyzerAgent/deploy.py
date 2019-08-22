#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

wappalyzerAgent = '''service wappalyzerAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/wappalyzerAgent.py -u
        port            = 11497
}
''' % cwd

wappalyzerService = 'wappalyzerAgent       11497/tcp                       # wappalyzerAgent\n'


open('/etc/xinetd.d/wappalyzerAgent','w').write(wappalyzerAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(wappalyzerService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

print ("Log Path is created")

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')
