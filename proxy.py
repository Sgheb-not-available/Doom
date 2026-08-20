import requests
import random
import json

class Proxy:
    def __init__(self):
        self.proxy = None
        self.proxy_list_base = [
            "32.223.6.94:80",
            "172.171.83.26:8080",
            "174.138.119.88:80",
            "47.253.201.85:7890",
            "50.122.86.118:80",
            "34.44.49.215:80",
            "109.199.119.160:80",
            "64.112.184.210:3128",
            "189.202.188.149:80",
            "24.63.14.91:8080",
        ]
        
        self.proxy_list_original = self.load_proxy_list()
        self.proxy_list_dinamic = self.proxy_list_original
        
    def get_proxy(self):
        if self.proxy:
            for i in range(len(self.proxy_list_dinamic)):
                if self.proxy == self.proxy_list_dinamic[i]:
                    self.proxy_list_dinamic.pop(i)
        
        while len(self.proxy_list_dinamic) > 0:
            i = random.randint(0, len(self.proxy_list_dinamic) - 2)
            proxy = self.proxy_list_dinamic[i]
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
                
            try:
                resp = requests.get("https://api.ipify.org?format=json",
                                    proxies=proxies,
                                    timeout=10)
                    
                print(f"Found working proxy: {proxy}")
        
                self.proxy = proxies
                return
            except requests.exceptions.RequestException:
                self.proxy_list_dinamic.pop(i)
                continue
        
        raise Exception("All available proxies are down, try again in a bit")  
    
    def save_proxy_list(self):
        with open("proxy.json", "w") as f:
            json.dump({"proxy_list": self.proxy_list_original}, f)

    def load_proxy_list(self) -> list:
        try:
            with open("proxy.json", "r") as f:
                raw = json.load(f)
                proxies = raw.get("proxy_list", [])
                return proxies if proxies else self.proxy_list_base
        except (FileNotFoundError, json.JSONDecodeError):
            return self.proxy_list_base