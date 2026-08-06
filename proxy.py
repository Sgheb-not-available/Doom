import requests
import random

def get_proxy(current) -> dict:
    proxy_list = [
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
    
    if current:
        for i in range(len(proxy_list)):
            if current == proxy_list[i]:
                proxy_list.pop(i)
    
    while len(proxy_list) > 0:
        i = random.randint(0, len(proxy_list) - 2)
        proxy = proxy_list[i]
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
            
        try:
            resp = requests.get("https://api.ipify.org?format=json",
                                proxies=proxies,
                                timeout=5)
                
            print(f"Found working proxy: {proxy}")
    
            return proxies
        except requests.exceptions.RequestException:
            proxy_list.pop(i)
            continue
    
    raise Exception("All available proxies are down, try again in a bit")  
    return {}