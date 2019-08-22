
import json
import psutil
# gives a single float value
psutil.cpu_percent()
# gives an object with many fields
psutil.virtual_memory()
# you can convert that object to a dictionary

output = dict()
output["memory"] = psutil.virtual_memory()._asdict()
output["cpu"] = psutil.cpu_percent(interval=0.1)
output["network"] = psutil.net_io_counters()._asdict()
output = json.dumps(output)
print(output)
