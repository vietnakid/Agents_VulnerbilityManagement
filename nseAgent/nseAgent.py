#!/usr/bin/env python3

import socket
import json
import os
import time
from lib import parserXML


class Nmap():
    def __init__(self):
        self.fileName = ""

    def gen_cmd(self, target, port):
        opt = ['nmap', '-oX', self.fileName, '-p', port, '--script=vuln,exploit', target, '> /dev/null 2>&1']
        cmd = ' '.join(opt)
        return cmd

    def gen_fileName(self, target, port):
        times = time.ctime()
        self.fileName = time.strftime('/var/log/nse/' + target + '_' + port + '_%Y%m%d-%H%M%S.xml')
        #self.fileName = 'testScript.xml'

    def runCmds(self, target, port):
        cmd = self.gen_cmd(target, port)
        os.system(cmd)

    def parse_XMLtoJson(self, target):
        result = parserXML.nmap_xml_to_json(self.fileName)
        if 'target' not in result:
            result['target'] = target
        _result = json.dumps(result)
        return _result


class Scan():
    def __init__(self, request):
        self.target = request.get('target', 'localhost')
        self.ports = request.get('openports', [])

    def run(self):
        results = dict()
        nm = Nmap()
        strListPort = ','.join(self.ports)
        nm.gen_fileName(self.target, strListPort)
        nm.runCmds(self.target, strListPort)
        results = nm.parse_XMLtoJson(self.target)
        print(results)


def main():
    # {"target": "localhost", "openports": ["631"]}
    # {"target": "192.168.31.12", "openports": ["80", "443"]}
    rawData = input()
    jData = json.loads(rawData)
    scan = Scan(jData)
    scan.run()


if __name__ == "__main__":
    main()
