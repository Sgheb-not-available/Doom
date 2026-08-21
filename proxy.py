import requests
import random
import json

from save_system.encryptor import encrypt, decrypt
from save_system.signer import SECRET_KEY

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
            i = random.randint(0, len(self.proxy_list_dinamic) - 1)
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
        data = [{"proxy_list": self.proxy_list_original}]
        payload = json.dumps(data)
        token = encrypt(payload, SECRET_KEY)
        with open("proxy.json", "w") as f:
            json.dump({"data": token}, f)

    def load_proxy_list(self) -> list:
        try:
            with open("proxy.json", "r") as f:
                raw = json.load(f)
            token = raw["data"]
            payload = decrypt(token, SECRET_KEY)
            data = json.loads(payload)
            return data if data else self.proxy_list_base
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return self.proxy_list_base
        except Exception:
            print("\nThe proxy save file was modified or corrupted. Delete your save file and restart the program. Closing Doom...")
            exit()