import subprocess
import json
import os

def main():
	targetJson = input()
	targetObject = json.loads(targetJson)
	openports = targetObject.get('openports')
	openports.append('')
	resultObject = dict()
	resultObject['result'] = dict()
	resultObject['target'] = targetObject.get('target')
	jobs = []
	prefix = ['http://', 'https://']
	for openport in openports:
		for pre in prefix:
			finalTarget = pre + targetObject.get('target') + ':' + openport + '/'
			cmd = ['wappalyzer', finalTarget]
			result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			jobs.append(result)
	for job in jobs:
		output = job.communicate()[0]
		_result = output.decode('utf-8')
		__result = json.loads(_result)
		finalTarget = list(__result.get('urls').keys())[0]
		if 'error' not in __result.get('urls').get(finalTarget):
			resultObject['result'][finalTarget] = __result
	print (json.dumps(resultObject.))

if __name__ == "__main__":
	main()
