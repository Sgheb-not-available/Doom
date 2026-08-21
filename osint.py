import time
import whois

from helper import *
from network import Network

class Osint:
    def __init__(self):
        self.network = Network()

    def profile_scan(self, name, proxy, timeout=5, max_retries=3):
        urls = {"Instagram": f"https://www.instagram.com/{name}/", 
                "Facebook": f"https://www.facebook.com/{name}/",
                "Github": f"https://www.github.com/{name}", 
                "Reddit": f"https://www.reddit.com/user/{name}/about.json",
                "TikTok": f"https://www.tiktok.com/@{name}",
                "Pinterest": f"https://www.pinterest.com/{name}/"}
        
        result = {}

        for key, url in urls.items():
            exists = False
            for attempt in range(max_retries):
                if not exists:
                    try:
                        r = requests.get(url, headers=self.network.headers, timeout=timeout, allow_redirects=True, proxies=proxy.proxy)
                    except requests.RequestException as e:
                        if attempt == max_retries:
                            print(f"{key}: Request failed: {e}")

                    if r.status_code == 200:
                        exists = "Sorry, this page isn't available" not in r.text
                    elif r.status_code == 404:
                        exists = False
                    elif r.status_code == 429:
                        wait = int(r.headers.get("Retry-After", 2 ** attempt)) + random.uniform(0, 1)
                        if attempt == max_retries:
                            print(f"{key}: Rate limited, waiting {wait:.1f}s...")
                        time.sleep(wait)
                        continue
                    else:
                        if attempt == max_retries:
                            print(f"{key}: Unexpected status: {r.status_code}")

            if not exists:
                print(f"{key}: Max retries exceeded")
            result[key] = exists
            
        print(f"\n{result}")
        
    def whois(self, domain): # proxy?                
        w = whois.whois(domain)
        if w.admin_name is not None:
            choice = input(f"The domain {domain} is owned by {w.admin_name}, do you want to see more? [y/n] ")
        else:
            choice = input(f"No admin name found for domain {domain}, do you want to see more anyway? [y/n] ")
        if choice == "y":
            print(f"\n{w}")
        