from lib import *
from Config import config
import json
import time
import signal

def run(address, scan_type):
	cf = config.Config()
	acunetix = Acunetix(username = cf.username, password = cf.password, domain = cf.domain, ssl_verify = cf.ssl_verify)
	try:
		acunetix.login()
		target = acunetix.create_target(address=address, description='Creating scan for ' + address)
		#print target
		target_id = target.get('target_id')
		#print target_id
		scan_id = acunetix.create_scan(target_id=target_id, scan_type=scan_type)
		objects = dict()
		objects['scan_details'] = list()
		#print scan_id
		while True:
			time.sleep(10)
			scan_stat = acunetix.scan_status(scan_id=scan_id, extra_stats=False)
			if scan_stat.get('status') == 'completed':
				break
			
		scan_vuls = acunetix.get_scan_vulnerabilities(scan_id=scan_id)
		#print scan_vuls
		for scan_vul in scan_vuls:
			vul_id = scan_vul.get('vuln_id')
			vuls_details = acunetix.get_vulnerability_by_id(scan_id=scan_id, vulnerability_id=vul_id)
			objects['scan_details'].append(vuls_details)
			#print vuls_details

		acunetix.delete_target(target_id)
		objects['target'] = address
		# objects['scan_type'] = scan_type
		print (json.dumps(objects))
	except KeyboardInterrupt:
		print("Interrupt received, stopping...")
	except Exception as e:
		error = {'error': e}
		print (json.dumps(error))
		pass
	finally:
		acunetix.logout()

def main():
	#{"scan_type": "High Risk Vulnerabilities", "target": "http://testphp.vulnweb.com"}
	rawData = input()
	jData = json.loads(rawData)
	scan_type = jData.get('scan_type')
	address = jData.get('target')
	if scan_type == 'Full Scan':
		scan_type = '11111111-1111-1111-1111-111111111111'
	elif scan_type == 'High Risk Vulnerabilities':
		scan_type = '11111111-1111-1111-1111-111111111112'
	elif scan_type == 'Cross-site Scripting Vulnerabilities':
		scan_type = '11111111-1111-1111-1111-111111111116'
	elif scan_type == 'SQL Injection Vulnerabilities':
		scan_type = '11111111-1111-1111-1111-111111111113'
	elif scan_type == 'Weak Passwords':
		scan_type = '11111111-1111-1111-1111-111111111115'
	elif scan_type == 'Crawl Only':
		scan_type = '11111111-1111-1111-1111-111111111117'

	run(address, scan_type)

if __name__ == "__main__":
	main()