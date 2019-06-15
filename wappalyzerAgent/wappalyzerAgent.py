import subprocess
import json
import os

def run_cmd(targetObject):
	prefix = ['http://', 'https://']
	for pre in prefix:
		finalTarget = pre + targetObject.get('target') + ':' + targetObject.get('port') + '/'
		cmd = ['wappalyzer', finalTarget]
		FNULL = open(os.devnull, 'w')
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=FNULL)
		_result = result.stdout.decode('utf-8')
		__result = json.loads(_result)
		if 'error' not in __result.get('urls').get(finalTarget):
			return __result
	return None

def main():
	targetJson = input()
	targetObject = json.loads(targetJson)
	openports = targetObject.get('openports')
	resultObject = dict()
	resultObject['result'] = dict()
	resultObject['target'] = targetObject.get('target')
	for i in openports:
		targetObject['port'] = str(i)
		_resultObject = run_cmd(targetObject)
		if _resultObject != None:
			resultObject['result'][i] = _resultObject

	print (json.dumps(resultObject))

if __name__ == "__main__":
	main()
