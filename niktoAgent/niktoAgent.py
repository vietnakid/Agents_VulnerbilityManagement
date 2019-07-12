#!/usr/bin/env python3

import json
import os
import time
import sys


class Nikto():
    def __init__(self):
        self.fileName = ""

    def gen_cmd(self, target):
        path = sys.argv[0].replace("niktoAgent.py", "")
        opt = ['perl', path + 'nikto/program/nikto.pl', '-host', target, '-o', self.fileName, '> /dev/null 2>&1']
        cmd = ' '.join(opt)
        return cmd

    def gen_fileName(self, target):
        times = time.ctime()
        self.fileName = time.strftime('/var/log/nikto/' + '_%Y%m%d-%H%M%S.json')

    def runCmds(self, target):
        cmd = self.gen_cmd(target)
        os.system(cmd)

    def fixJson(self, target):
        try:
            with open(self.fileName, 'r') as js:
                result = js.read()
                result = result.replace(',]', ']').replace(',}', '}')
        except Exception as e:
            return json.dumps({'error': e})
        return result


class Scan():
    def __init__(self, request):
         # "newScan" default type scan
        self.type = request.get('type', "newScan")
        # "localhost" default target scan
        self.target = request.get('target_url', "localhost")

    def run(self):
        if self.type == "newScan":
            self.newScan()
        else:
            print('Not found')

    def newScan(self):
        nikto = Nikto()
        nikto.gen_fileName(self.target)
        nikto.runCmds(self.target)
        result = nikto.fixJson(self.target)
        print(result)


def main():
    # {"type": "newScan", "target": "https://nz4.xyz/getLink"}
    rawData = input()
    jData = json.loads(rawData)
    scan = Scan(jData)
    scan.run()


if __name__ == "__main__":
    main()
