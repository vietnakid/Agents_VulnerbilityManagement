#!/usr/bin/python3
#coding=utf8

import os
from os import system
import sys

cwd = os.getcwd()

cveSearchAgent = '''service cveSearchAgent
{
        socket_type     = stream
        protocol        = tcp
        user            = root
        wait            = no
        server          = /usr/bin/python3
        server_args     = %s/cveSearchAgent.py -u
        port            = 25799
}
''' % cwd

cveSearchService = 'cveSearchAgent       25799/tcp                       # cveSearchAgent\n'


open('/etc/xinetd.d/cveSearchAgent','w').write(cveSearchAgent)
print('[OK] Added to xinetd.d')

open('/etc/services','a').write(cveSearchService)
print('[OK] Added new service to /etc/services')

system('/etc/init.d/xinetd restart')

# create Log Path
path = "/var/log/cveSearch"
os.mkdir(path)

print ("Log Path is created")

print('''
============================
||  [+] Deploy finish :)  ||
============================
''')