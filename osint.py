import time
import whois
import os

from helper import *

class Osint:
    def profile_scan(self, name, proxy, timeout=5, max_retries=3):
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

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
                        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, proxies=proxy)
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
        
    def whois(self, domain):                
        w = whois.whois(domain)
        if w.admin_name is not None:
            choice = input(f"The domain {domain} is owned by {w.admin_name}, do you wish to see more? [y/n] ")
        else:
            choice = input(f"No admin name found for domain {domain}, do you want to see more anyway? [y/n] ")
        if choice == "y":
            print(f"\n{w}")
        