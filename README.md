# Agents_VunerbilityManagement
Agents_VunerbilityManagement

### Deploy Agent

* For Nmap Agent:
	* Run file `install.sh` as root user in folder `nmapAgent`

* For NSE Agent:
	* Run file `install.sh` as root user in folder `nseAgent`

* For Wappalyzer Agent:
	* Install nodejs and npm first (Google search for this step)
	* Use npm to install wappalyzer package in `https://www.npmjs.com/package/wappalyzer` by this command `npm i -g wappalyzer`
	* Change directory to `wappalyzerAgent` and run `python3 deploy.py`

* For CVE-Search Agent:
	* If you not using docker, you have to re-configure in the deploy.py file. We recommend to use docker at here: https://hub.docker.com/r/ttimasdf/cve-search/
	* Install xinetd
	* Change directory to `cveSearchAgent` and run `python3 deploy.py`

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
	* Run file `install.sh` as root user in folder `niktoAgent`