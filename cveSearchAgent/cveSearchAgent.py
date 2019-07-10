import json
import subprocess
import traceback

def main():
    jData = input()
    data = json.loads(jData)

    cpes = data.get('cpes', [])
    jobs = []

    for cpe in cpes:
        cmd = ['python3', '/opt/cve/bin/search.py', '-p', cpe, '-o', 'json']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        jobs.append((cpe, process))

    outputResult = []
    
    for job in jobs:
        try:
            process = job[1]
            jOutputs = process.communicate()[0].decode('utf-8').split('\n')
            cpe = job[0]
            for jOutput in jOutputs:
                try:
                    output = json.loads(jOutput)
                    res = dict()
                    res['cve'] = output.get("id")
                    res['cvss'] = output.get("cvss")
                    res['cwe'] = output.get("cwe")
                    res['cpe'] = cpe
                    outputResult.append(res)
                except Exception as e:
                    pass
        except Exception as e:
            print("Exception =", e)
            traceback.print_exc()
    print(json.dumps(outputResult))

if __name__ == "__main__":
    # {"cpes": ["python:3.6.5", "excel"]}
    main()
