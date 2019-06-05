#!/usr/bin/env python3

import socket
import json
import pickle
import nmap
import os
import time
import xmltodict


class Nmap():
    def __init__(self):
        self.fileName = ""

    def gen_cmd(self, target):
        opt = ['nmap', '-oX', self.fileName, '-A', target]
        cmd = ' '.join(opt)
        return cmd

    def gen_fileName(self):
        times = time.ctime()
        self.fileName = time.strftime('%Y%m%d-%H%M%S.txt')

    def runCmds(self, target):
        cmd = self.gen_cmd(self.fileName)
        os.system(cmd)
        
    def parse_XMLtoJson(self):
        f = open(self.fileName)
        xml_content = f.read()
        f.close()
        result = json.dumps(xmltodict.parse(
            xml_content, xml_attribs=True), indent=4, sort_keys=True)
        return result


def main():
    target = input()
    nm = Nmap()
    nm.gen_fileName()
    nm.runCmds(target)
    result = nm.parse_XMLtoJson()
    print(result)


if __name__ == "__main__":
    main()
