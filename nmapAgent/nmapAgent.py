#!/usr/bin/env python3

import socket
import json
import os
import time
from lib import parserXML


class Nmap():
    def __init__(self):
        self.fileName = ""

    def gen_cmd(self, target):
        opt = ['nmap', '-sV', '-oX', self.fileName, '--top-ports 1000', '-p 1-10000', '-T4', target, '> /dev/null 2>&1']
        cmd = ' '.join(opt)
        return cmd

    def gen_fileName(self, target):
        times = time.ctime()
        self.fileName = time.strftime('/var/log/nmap/' + target + '_%Y%m%d-%H%M%S.xml')

    def runCmds(self, target):
        cmd = self.gen_cmd(target)
        os.system(cmd)

    def parse_XMLtoJson(self):
        result = json.dumps(parserXML.nmap_xml_to_json(self.fileName))
        return result


class Scan():
    def __init__(self, request):
         # "newScan" default type scan
        self.type = request.get('type', "newScan")
        # "localhost" default target scan
        self.target = request.get('target', "localhost")

    def run(self):
        if self.type == "newScan":
            self.newScan()
        elif self.type == "reScan":
            print('reScan Cumming')
        else:
            print('Not found')

    def newScan(self):
        nm = Nmap()
        nm.gen_fileName(self.target)
        nm.runCmds(self.target)
        result = nm.parse_XMLtoJson()
        f = open(nm.fileName + '.txt', "w")
        f.write(result)
        f.close()
        print(result)


def main():
    # {"type": "newScan", "target": "nmap.org"}
    rawData = input()
    jData = json.loads(rawData)
    scan = Scan(jData)
    scan.run()


if __name__ == "__main__":
    main()
