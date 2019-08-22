from lib import *
from Config import config
import json
import time
import signal
import pickle
import traceback

def save_object(obj):
	try:
		with open('./obj_acu.pkl', 'wb') as obj_file:
			pickle.dump(obj, obj_file)
	except:
		return None

def load_object():
	try:
		with open('./obj_acu.pkl', 'rb') as obj_file:
			obj = pickle.load(obj_file)
			return (obj)
	except:
		return None

def run(address, scan_type):
	cf = config.Config()
	acunetix = Acunetix(username = cf.username, password = cf.password, domain = cf.domain, ssl_verify = cf.ssl_verify)
	try:
		_acunetix = load_object()
		if _acunetix != None:
			_acunetix.url = 'https://' + cf.domain
			if _acunetix.check_logging() == False:
				acunetix.login()
				save_object(acunetix)
			else:
				acunetix = _acunetix
		else:
			acunetix.login()
			save_object(acunetix)
		target = acunetix.create_target(address=address, description='Creating scan for ' + address)
		# print (target)
		target_id = target.get('target_id')
		#print target_id
		scan_id = acunetix.create_scan(target_id=target_id, scan_type=scan_type)
		objects = dict()
		objects['scan_details'] = list()
		#print scan_id
		while True:
			time.sleep(10)
			# print (acunetix.check_logging())
			scan_stat = acunetix.scan_status(scan_id=scan_id, extra_stats=False)
			if scan_stat.get('status') == 'completed':
				break
		
		scan_stat = acunetix.scan_status(scan_id=scan_id, extra_stats=True)
		objects['scan_stat'] = scan_stat

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
		error = {'error': str(e), 'traceback': traceback.format_exc()}
		print (json.dumps(error))
		pass
	finally:
		# acunetix.logout()
		pass

def main():
	#{"acunetix_scan_type": "High Risk Vulnerabilities", "target_url": "http://testphp.vulnweb.com"}
	rawData = input()
	jData = json.loads(rawData)
	scan_type = jData.get('acunetix_scan_type')
	address = jData.get('target_url')
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