import requests
import time

class Nessus(requests.Session):
    def __init__(self, username=None, password=None, accessKey=None, secretKey=None, domain=None, ssl_verify=True, X_API_Token=None, *args, **kwargs):
        if not domain:
            raise ValueError("domain are required")
        if not ((username and password) or (accessKey and secretKey)):
            raise ValueError("username, password or APIKeys are required")
        requests.packages.urllib3.disable_warnings()
        super(Nessus, self).__init__()
        url = ["https://", domain]

        self.verify = ssl_verify
        self.timeout = 5
        self.headers = {
            "Accept": "application / json, text / plain, * / *",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.authenticated = False
        self.max_redirects = 0
        self.headers.update({"X-API-Token": X_API_Token})
        self.url = "".join(url)
        if username and password:
            self.username = username
            self.password = password
        elif accessKey and secretKey:
            self.accessKey = accessKey
            self.secretKey = secretKey
            apiKeys = ["accessKey=" + accessKey, "secretKey=" + secretKey]
            self.headers.update({"X-ApiKeys": ';'.join(apiKeys)})
            if not self.check_logging():
                raise Exception('X-ApiKeys is not working')
        self.check_connectivity()

    def request(self, *args, **kwargs):
        try:
            return super(Nessus, self).request(timeout=5, *args, **kwargs)
        except Exception as e:
            raise e

    def check_connectivity(self):
        try:
            url = self.url + "/server/status"
            resp = self.get(url)
            if resp.status_code == 200:
                return resp.json()['status']
        except Exception as e:
            raise e

    def check_logging(self):
        while True:
            try:
                url = self.url + "/session"
                resp = self.get(url)
                if 'Invalid Credentials' not in resp.text:
                    self.authenticated = True
                    return True
                return False
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except:
                return False

    def login(self):
        while True:
            try:
                url = self.url + "/session"
                data = {"username": self.username, "password": self.password}
                resp = self.post(url, json=data)
                if resp.status_code == 200:
                    token = resp.json()['token']
                    self.authenticated = True
                    self.headers.update({"X-Cookie": "token=" + token})
                    return True
                else:
                    raise Exception('Failed to authenticate')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def logout(self):
        while True:
            try:
                url = self.url + "/session"
                resp = self.delete(url)
                if resp.status_code == 200:
                    return True
                else:
                    raise Exception('Failed to logout')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def create_scan(self, target, uuid, ports):
        while True:
            try:
                url = self.url + "/scans"
                setting = {
                    "name": target,
                    "text_targets": target,
                    "launch_now": True,
                    "portscan_range": ports
                }
                data = {"uuid":uuid, "settings": setting}
                resp = self.post(url, json=data)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to create scan')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def delete_scan(self, scan_id):
        while True:
            try:
                url = self.url + "/scans/" + str(scan_id)
                resp = self.delete(url)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to delete scan')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def launch_scan(self, scan_id):
        while True:
            try:
                url = self.url + "/scans/" + str(scan_id) + "/launch"
                resp = self.post(url)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to launch scan')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def stop_scan(self, scan_id):
        while True:
            try:
                url = self.url + "/scans/" + str(scan_id) + "/stop"
                resp = self.post(url)
                if resp.status_code == 200:
                    return
                raise Exception('Failed to stop scan')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def details_scan(self, scan_id):
        while True:
            try:
                url = self.url + "/scans/" + str(scan_id)
                resp = self.get(url)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to get scan details')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def plugins_details(self, scan_id, plugin):
        while True:
            try:
                url = self.url + "/scans/" + str(scan_id) + "/plugins/" + str(plugin)
                resp = self.get(url)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to get plugin details')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def list_template_scan(self):
        while True:
            try:
                url = self.url + "/editor/scan/templates"
                resp = self.get(url)
                if resp.status_code == 200:
                    return resp.json()
                raise Exception('Failed to get list template')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

