from xml.etree import ElementTree as ET
import json

def get_status(nmapFile):
	scan_result = {}
	with open(nmapFile) as f:
		nmap_xml_output = f.read()
	
	if nmap_xml_output is not None:
		_nmap_last_output = nmap_xml_output
	else:
		return returnError('XML does not exists')

	try:
		dom = ET.fromstring(_nmap_last_output)
	except Exception as e:
		return returnError(e)

	dhosts = dom.find("runstats/hosts")
	if dhosts != None:
		up = dhosts.get('up')
		down = dhosts.get('down')
	else:
		return returnError('Could\'t find up and down status')

	if up == '0' and down == '0':
		return returnError('Nmap error, 0 up 0 down')
	elif down == '1':
		scan_result = {'status': 'hostDown'}
		return scan_result

	scan_result['status'] = 'hostUp'

	dfinished = dom.find("runstats/finished")
	if dfinished != None:
		scan_result['scanstats'] = {
			'timestr':dfinished.get('timestr'),
			'elapsed':dfinished.get('elapsed'),
			'time':dfinished.get('time')
			}
	else:
		return returnError('Nmap did not finished')
	return scan_result

def nmap_xml_to_json(nmapFile):
	scan_result = {}
	#open nmap file
	with open(nmapFile) as f:
		nmap_xml_output = f.read()
	
	if nmap_xml_output is not None:
		_nmap_last_output = nmap_xml_output
	else:
		return returnError('XML does not exists')

	try:
		dom = ET.fromstring(_nmap_last_output)
	except Exception as e:
		return returnError(e)

	# dhosts = dom.find("runstats/hosts")
	# if dhosts != None:
	# 	up = dhosts.get('up')
	# 	down = dhosts.get('down')
	# else:
	# 	return returnError('Could\'t find up and down status')

	# if up == '0' and down == '0':
	# 	return returnError('Nmap error, 0 up 0 down')
	# elif down == '1':
	# 	scan_result = {'status': 'hostDown'}
	# 	return scan_result

	# scan_result['status'] = 'hostUp'

	# dfinished = dom.find("runstats/finished")
	# if dfinished != None:
	# 	scan_result['scanstats'] = {
	# 		'timestr':dfinished.get('timestr'),
	# 		'elapsed':dfinished.get('elapsed'),
	# 		'time':dfinished.get('time')
	# 		}
	# else:
	# 	return returnError('Nmap did not finished')


	# dhost = dom.find("host")
	# if dhost != None:
	# 	if dhost.find("address") != None:
	# 		scan_result['target'] = dhost.find("address").get('addr')
	# 	else:
	# 		return returnError('Nmap error, not found IP in XML file')
	# 	if dhost.find("hostnames/hostname") != None:
	# 		scan_result['hostname'] = dhost.find("hostnames/hostname").get('name')
	# 	else:
	# 		scan_result['hostname'] = None

	dports = dom.findall('host/ports/port')
	for i in dports:
		portid = i.get('portid')
		dscript = i.findall('script')
		if dscript != None:
			for j in dscript:
				script = j.get('id')
				output = j.get('output')
		else:
			script = None
			output = None

		scan_result[portid] = {
			'script': script,
			'output': output
		}

	return scan_result

def returnError(error):
	scan_result = {'status': 'error', 'detail': error}
	return scan_result

#print (nmap_xml_to_json('testScript.xml'))
