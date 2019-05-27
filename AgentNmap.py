
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
         ip= request["ip"]
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

def Main():

    host = '127.0.0.1'

    port = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    s.listen()
    c,addr = s.accept()
    print('Connected to :', addr[0], ':', addr[1])
    
    data = c.recv(1024).decode('utf-8')      
    print(data)

    jdata= json.loads(data)

    r =Run()
    result =r.scan_options(jdata)
    print(result)

    c.send(result.encode('utf-8'))

    s.close()


if __name__ == '__main__':
    Main()
