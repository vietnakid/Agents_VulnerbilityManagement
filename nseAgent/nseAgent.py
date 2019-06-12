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
        opt = ['nmap', '-oX', self.fileName, '-p', port, '--script=default,vuln,exploit', target, '> /dev/null 2>&1']
        cmd = ' '.join(opt)
        return cmd

    def gen_fileName(self, target, port):
        times = time.ctime()
        self.fileName = time.strftime('/var/log/nse/' + target + '_' + port + '_%Y%m%d-%H%M%S.xml')
        #self.fileName = 'testScript.xml'

    def runCmds(self, target, port):
        cmd = self.gen_cmd(target, port)
        os.system(cmd)

    def parse_XMLtoJson(self):
        result = json.dumps(parserXML.nmap_xml_to_json(self.fileName))
        return result


class Scan():
    def __init__(self, request):
        self.target = request.get('target', 'localhost')
        self.ports = request.get('openports', {})

    def run(self):
        results = dict()
        nm = Nmap()
        results['target'] = self.target
        listPort = list()
        for port in self.ports:
            listPort.append(port)
        strListPort = ','.join(listPort)
        nm.gen_fileName(self.target, listPort)
        nm.runCmds(self.target, listPort)
        result = nm.parse_XMLtoJson()
        results.update(json.loads(result))

        print(json.dumps(results))


def main():
    # {"type": "newScan", "target": "nmap.org"}
    rawData = input()
    jData = json.loads(rawData)
    scan = Scan(jData)
    scan.run()


if __name__ == "__main__":
    main()
