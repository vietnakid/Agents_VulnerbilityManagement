# Agents_VunerbilityManagement
Agents_VunerbilityManagement

##Install
###Install requirement tools
* Agent machine need to install: nmap, xinetd and python3
```
sudo apt-get update
sudo apt-get install nmap xinetd python3 -y
```

* Create folder to store log file:
```
mkdir -p /var/log/nmap
mkdir -p /var/log/nse
```

###Deploy Agent

* For Nmap Agent:
	Change directory to `nmapAgent` and run `python3 deploy.py`

* For NSE Agent:
	Change directory to `nseAgent` and run `python3 deploy.py`