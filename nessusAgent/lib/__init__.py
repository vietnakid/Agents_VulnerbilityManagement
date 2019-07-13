import requests
import time

class Nessus(requests.Session):
    def __init__(self, username=None, password=None, domain=None, ssl_verify=True, X_API_Token=None, *args, **kwargs):
        if any([not username, not password, not domain]):
            raise ValueError("username, password and domain are required")
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
        self.username = username
        self.password = password
        self.X_API_Token = X_API_Token
        self.url = "".join(url)
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

    def login(self):
        while True:
            try:
                url = self.url + "/session"
                data = {"username": self.username, "password": self.password}
                resp = self.post(url, json=data)
                if resp.status_code == 200:
                    token = resp.json()['token']
                    self.authenticated = True
                    self.headers.update({"X-API-Token": self.X_API_Token})
                    self.headers.update({"X-Cookie": "token=" + token})
                    # print (self.headers)
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
                # print (self.headers)
                resp = self.delete(url)
                # print (resp.text)
                if resp.status_code == 200:
                    return True
                else:
                    raise Exception('Failed to logout')
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                pass
            except Exception as e:
                raise e

    def create_scan(self, target, uuid):
        while True:
            try:
                url = self.url + "/scans"
                setting = {
                    "name": target,
                    "text_targets": target,
                    "launch_now": True
                }
                data = {"uuid":uuid, "settings": setting}
                # print (json.dumps(data))
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

