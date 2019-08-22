#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

nseAgent = '''service nseAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/nseAgent.py -u
        port            = 25798
}
''' % cwd

nseService = 'nseAgent       25798/tcp                       # nseAgent\n'


open('/etc/xinetd.d/nseAgent','w').write(nseAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(nseService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

# create Log Path
path = "/var/log/nse"
os.mkdir(path)

print ("Log Path is created")

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')