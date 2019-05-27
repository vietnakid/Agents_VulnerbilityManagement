import socket
import json
import pickle
import nmap

class Nmap():
    def nmap_scanFull(self,ip):
        nm =nmap.PortScanner()
        jdata = json.dumps(nm.scan(ip),indent=4)
        print(type(jdata))
        return jdata

    def nmap_detectOS(self,ip):
        nm =nmap.PortScanner()
        jdata = json.dumps(nm.scan(ip, arguments='-O' ),indent=4)
        return jdata

    def nmap_PortRangeScan(self,ip):
        nm =nmap.PortScanner()
        jdata = json.dumps(nm.scan(ip, arguments="-sn -n -T5"),indent=4)
        return jdata

class Run():
    def format_Actions(self,request):
        actions_String= request['actions']
        list_actions= actions_String.split(',')
        for i,item in enumerate (list_actions):
            list_actions[i] =list_actions[i].strip()
        return list_actions
    def scan_options(self,request):
         nm= Nmap()
         result = {
             "Status" :"OK"
         }
         ip = request["ip"]
         actions =self.format_Actions(request)
         if (len(actions)>0):
             for ac in actions:
                if(ac == "scan"):
                     result_scan= json.loads(nm.nmap_scanFull(ip))
                     result.update(result_scan)
                if (ac == "os"):
                     result_OS = json.loads(nm.nmap_detectOS(ip))
                     result.update(result_OS)
                if (ac == "port"):
                     result_port = json.loads(nm.nmap_PortRangeScan(ip))
                     result.update(result_port)
         return json.dumps(result,indent=4)

def main():
    rawData = input()
    jData = json.loads(rawData)
    r = Run()
    result =r.scan_options(jData)
    print(result)
    

if __name__ == "__main__":
    main()

