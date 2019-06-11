from xml.etree import ElementTree as ET
import json

def nmap_xml_to_json(nmapFile):
	scan_result = {}
	with open(nmapFile) as f:
		nmap_xml_output = f.read()

	if nmap_xml_output is not None:
		_nmap_last_output = nmap_xml_output
	else:
		scan_result = {'status': 'error', 'detail': 'XML does not exists'}
		return scan_result

	try:
		dom = ET.fromstring(_nmap_last_output)
	except Exception as e:
		scan_result = {'status': 'error', 'detail': e}
		return scan_result

	up = dom.find("runstats/hosts").get('up')
	down = dom.find("runstats/hosts").get('down')

	if up == '0' and down == '0':
		scan_result = {'status': 'error', 'detail': 'Nmap error, 0 up 0 down'}
		return scan_result
	elif down == '1':
		scan_result = {'status': 'hostDown'}
		return scan_result

	scan_result['status'] = 'hostUp'
	scan_result['scanstats'] = {
		'timestr':dom.find("runstats/finished").get('timestr'),
		'elapsed':dom.find("runstats/finished").get('elapsed'),
		'time':dom.find("runstats/finished").get('time')
		}


	dhost = dom.find("host")
	if dhost != None:
		if dhost.find("address") != None:
			scan_result['ip'] = dhost.find("address").get('addr')
		else:
			scan_result = {'status': 'error', 'detail': 'Nmap error, not found IP in XML file'}
			return scan_result
		if dhost.find("hostnames/hostname") != None:
			scan_result['hostname'] = dhost.find("hostnames/hostname").get('name')
		else:
			scan_result['hostname'] = None

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

#print (nmap_xml_to_json('vlxx.com_20190609-171213.xml'))
#print (nmap_xml_to_json('10.22.194.10_20190611-140746.xml'))
