# Agents_VunerbilityManagement
Agents_VunerbilityManagement

### Deploy Agent

* For Nmap Agent:
	* Run file `install.sh` in folder `nmapAgent` as root user

* For NSE Agent:
	* Run file `install.sh` in folder `nmapAgent` as root user

* For Wappalyzer Agent:
	* Run file `install.sh` in folder `wappalyzerAgent` as root user

* For CVE-Search Agent:
	* If you not using docker, you have to re-configure in the deploy.py file. We recommend to use docker at here: https://hub.docker.com/r/ttimasdf/cve-search/
	* Run file `install.sh` in folder `cveSearchAgent` as root user

* For Acunetix Agent:
	* If you already have Acunetix, please fill your login to Acunetix in `Config/config.py`
	* If you don't have Acunetix, we recommend you to use docker at here to try free for 14 days: `https://hub.docker.com/r/dictcp/acunetix`
	* Run file `install.sh` as root user in folder `acunetixhAgent`

* For Nessus Agent:
	* If you already have Nessus:
		* Please fill your `login` or `token` Nessus in `Config/config.py`
		* `X_API_Token` in `Config/config.py` is required, it appear in header when you make a request to Nessus
	* If you don't have Nessus, we recommend you to use docker at here to try free for 7 days: `docker run -dt -p 8834:8834 -e ADMIN_USER=admin -e ADMIN_PASS=admin -e LICENSE={license-key} --name nessus_scanner stevemcgrath/nessus_scanner:latest`
	* Run file `install.sh` as root user in folder `nessusAgent`

* For Nikto Agent:
	* Run file `install.sh` in folder `niktoAgent` as root user