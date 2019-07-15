from lib import *
from Config import config
import json
import time
import traceback

def run(target, scan_type, ports):
    cf = config.Config()
    try:
        if cf.username and cf.password:
            ns = Nessus(username = cf.username, password = cf.password, domain = cf.domain, ssl_verify = cf.ssl_verify, X_API_Token=cf.X_API_Token)
            ns.login()
        elif cf.token:
            ns = Nessus(token = cf.token, domain = cf.domain, ssl_verify = cf.ssl_verify, X_API_Token=cf.X_API_Token)
        scan = ns.create_scan(target=target, uuid=scan_type, ports=ports)
        scan_id = scan['scan']['id']
        while True:
            details_scan = ns.details_scan(scan_id)
            if len(details_scan['hosts']) > 0 and 'scanprogresscurrent' in details_scan['hosts'][0] and details_scan['hosts'][0]['scanprogresscurrent'] == 99:
                ns.stop_scan(scan_id)
                break
            time.sleep(5)

        objects = dict()
        objects['scan_details'] = list()
        objects['target'] = target
        for scan_vul in details_scan['vulnerabilities']:
            vuls_details = ns.plugins_details(scan_id, scan_vul['plugin_id'])
            objects['scan_details'].append(vuls_details)
            break
        print (json.dumps(objects))
    except Exception as e:
        error = {'error': str(e), 'traceback': traceback.format_exc()}
        print (json.dumps(error))
        pass
    finally:
        try:
            ns.logout()
        except:
            pass

def main():
    #{"nessus_scan_type": "Basic Network Scan", "target": "192.168.31.248", "ports": ["8881", "6969"]}
    rawData = input()
    jData = json.loads(rawData)
    scan_type = jData.get('nessus_scan_type')
    address = jData.get('target')
    ports = jData.get('ports')
    _ports = ','.join(ports)
    if scan_type == 'Advanced Scan':
        scan_type = 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66'
    elif scan_type == 'Basic Network Scan':
        scan_type = '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    else:
        scan_type = '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    
    run(address, scan_type, _ports)

if __name__ == "__main__":
    main()