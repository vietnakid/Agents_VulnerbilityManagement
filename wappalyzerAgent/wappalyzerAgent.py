import subprocess
import json
import os
import time

def normalizeOutputData(outputData):
	# reconstruct application to array
	applications = outputData.get('applications')
	
	finalApplications = []
	for application in applications:
		categories = application.get('categories')
		finalCategories = []
		for category in categories:
			for categoryName in category.values():
				finalCategories.append(categoryName)
		application['categories'] = finalCategories

		application['confidence'] = int(application.get('confidence'))
		finalApplications.append(application)
	outputData['applications'] = finalApplications

	# del "meta" key
	if 'meta' in outputData:
		del outputData['meta']

	# reconstruct "urls"
	urls = outputData.get('urls')
	port = None
	path = '/'
	for url in urls:
		url = url.split('/')
		if len(url[2].split(':')) == 2:
			port = url[2].split(':')[1]
		path = '/'.join(url[3:])
	if 'urls' in outputData:
		del outputData['urls']

	outputData['port'] = port
	outputData['path'] = path
	return outputData

def main():
	targetJson = input()
	targetObject = json.loads(targetJson)
	openports = targetObject.get('openports')
	openports.append('')
	resultObject = dict()
	resultObject['result'] = []
	resultObject['target'] = targetObject.get('target')
	jobs = []
	prefix = ['http://']
	commonPaths = ['', 'admin', 'login', 'admin.php', 'login.php']
	for openport in openports:
		for pre in prefix:
			for commonPath in commonPaths:
				finalTarget = pre + targetObject.get('target') + ':' + openport + '/' + commonPath
				# finalTarget = targetObject.get('target')
				cmd = ['wappalyzer', finalTarget]
				result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				jobs.append(result)
				time.sleep(1) # Wait for wappalyzer to send request, if we dont wait, the result can be incorrect

	solvePort = []
	for job in jobs:
		try:
			output = job.communicate()[0]
			_result = output.decode('utf-8')
			__result = json.loads(_result)
			finalTarget = list(__result.get('urls').keys())[0]
			if 'error' not in __result.get('urls').get(finalTarget):
				normalizedData = normalizeOutputData(__result)
				port = str(normalizedData.get('port'))
				path = normalizedData.get('path')
				if port+path not in solvePort:
					solvePort.append(port+path)
					resultObject['result'].append(normalizedData)
		except:
			pass
	print (json.dumps(resultObject))

if __name__ == "__main__":
	# {"target": "testphp.vulnweb.com", "hostname": "testphp.vulnweb.com", "openports": ["80", "443"]}
	main()
