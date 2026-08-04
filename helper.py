import requests
import socket

"""
NETWORK
"""

def check_connection(self) -> bool:
    try:
        res = requests.get("http://www.google.com")
        if res.status_code == 200:
            return True
    except:
        return False

def connect_tcp(self, host, port, timeout) -> tuple:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(timeout)
        connection = s.connect((host, int(port)))
        return (host, port)
    except (ConnectionRefusedError, OSError):
        return None
    finally:
        s.close()
        
def connect_tcp_thread(self, host, open_ports, port):
    connection = connect_tcp(self, host, port, 10)
                        
    if connection:
        open_ports.append(port)
        
def get_host(self, domain) -> str:
    try:
        host = socket.gethostbyname(domain)
        return host
    except socket.gaierror:
        return None
    
def get_domain(self, ip) -> str:
    try:
        domain = socket.gethostbyaddr(ip)[0]
        return domain
    except socket.herror:
        return None
    
"""
OSINT
"""
    
def check_instagram(self, name, timeout=5) -> bool:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459",
        "Accept": "application/json",
    }

    api_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={name}"

    try:
        r = requests.get(api_url, headers=HEADERS, timeout=timeout)
        print(r)
    except requests.RequestException:
        return False 

    if r.status_code != 200:
        return False

    try:
        data = r.json()
    except ValueError:
        return False

    return data.get("data", {}).get("user") is not None

"""
OTHER
"""
 
def split_threads(self, threads, next_threads):
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    for t in next_threads:
        t.start()
        
    for t in next_threads:
        t.join()