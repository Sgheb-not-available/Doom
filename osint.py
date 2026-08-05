from helper import *

class Osint:
    def profile_scan(self, name, use_proxy, timeout=5, max_retries=3):
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
        
        proxy = None
        if use_proxy:
            proxy = get_proxy()

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