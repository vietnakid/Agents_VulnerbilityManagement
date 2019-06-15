from xml.etree import ElementTree as ET
import json

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

	dhosts = dom.find("runstats/hosts")
	if dhosts != None:
		up = dhosts.get('up')
		down = dhosts.get('down')
	else:
		return returnError('Couldn\'t find up and down status')

	dfinished = dom.find("runstats/finished")
	if dfinished != None:
		scan_result['scanstats'] = {
			'elapsed':dfinished.get('elapsed'),
			'time':dfinished.get('time')
			}
	else:
		return returnError('Nmap did not finished')

	if up == '0' and down == '0':
		return returnError('Nmap error, 0 up 0 down')
	elif down == '1':
		scan_result['status'] = 'hostDown'
		scan_result['openports'] = {}
		return scan_result

	scan_result['status'] = 'hostUp'


	dhost = dom.find("host")
	if dhost != None:
		if dhost.find("address") != None:
			scan_result['target'] = dhost.find("address").get('addr')
		else:
			return returnError('Nmap error, not found IP in XML file')
		if dhost.find("hostnames/hostname") != None:
			scan_result['hostname'] = dhost.find("hostnames/hostname").get('name')
		else:
			scan_result['hostname'] = None
	else:
		return returnError('Nmap error, nmap did not finished')

	openports = {}
	dports = dom.findall('host/ports/port')
	for i in dports:
		portid = i.get('portid')
		dservice = i.find('service')
		if dservice != None:
			product = dservice.get('product')
			version = dservice.get('version')
			extrainfo = dservice.get('extrainfo')
			ostype = dservice.get('ostype')
			method = dservice.get('method')
			conf = dservice.get('conf')
			dcpe = dservice.findall('cpe')
			cpes = []
			for j in dcpe:
				cpes.append(j.text)
		else:
			product = None
			version = None
			extrainfo = None
			ostype = None
			method = None
			conf = None
			dcpe = None
			cpes = []

		openports[portid] = {
			'product': product,
			'version': version,
			'extrainfo': extrainfo,
			'ostype': ostype,
			'method': method,
			'conf': conf,
			'cpe': cpes
		}

	scan_result['openports'] = openports

	return scan_result

def returnError(error):
	scan_result = {'status': 'error', 'detail': error}
	return scan_result

#print (json.dumps(nmap_xml_to_json('testScript.xml')))
