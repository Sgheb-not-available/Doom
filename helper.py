import requests
import socket
import re

from proxy import *

"""
NETWORK
"""
    
def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()

def connect_tcp(host, port, timeout=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(timeout)
        connection = s.connect((host, int(port)))
        try:
            banner = s.recv(1024).decode()
            return (host, port), banner
        except:
            return (host, port)
    except (ConnectionRefusedError, OSError):
        return None
    finally:
        s.close()
        
def probe_udp(host, port, timeout=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(b"", (host, int(port)))
        banner = s.recvfrom(1024)
        return port, banner
    except (socket.timeout, ConnectionRefusedError):
        return None
    finally:
        s.close()
        
def connect_tcp_thread(host, open_ports, port):
    try:
        connection, banner = connect_tcp(host, port)
    except TypeError:
        connection = None
                        
    if connection:
        open_ports[port] = banner
        
def probe_udp_thread(host, open_ports, port):
    try:
        port, banner = probe_udp(host, port)
    except TypeError:
        port = None
        banner = None
        
    if port:
        open_ports[port] = banner
        
def get_host(domain) -> str:
    try:
        host = socket.gethostbyname(domain)
        return host
    except socket.gaierror:
        return None
    
def get_domain(ip) -> str:
    try:
        domain = socket.gethostbyaddr(ip)[0]
        return domain
    except socket.herror:
        return None
    
def get_content(address, proxy, d_ipv4):
    try:
        if not proxy.proxy:
            choice = input("\nYou have no active proxy, do you want to use one before grabbing the content of this web page? [y/n] ")
            if choice == "y":
                proxy.get_proxy()
        if d_ipv4 and bool(re.match(d_ipv4, address)):
            address = get_domain(address)
        r = requests.get(f"http://{address}", proxies=proxy.proxy)
        if r.status_code == 200:
            print(f"\n{r.content.strip()}")
        else:
            print(f"There was an error while to get the content of {address}, code: {r.status_code}")
    except requests.exceptions.SSLError:
        print(f"An SSL error occourred while trying to fetch the content of {address}")

"""
OTHER
"""

def print_doom():
    print(r"""
██████╗  ██████╗  ██████╗ ███╗   ███╗
██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║  ██║██║   ██║██║   ██║██╔████╔██║
██║  ██║██║   ██║██║   ██║██║╚██╔╝██║
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
     """)
    
def print_cmds():
    print("""
Available commands:
scanner
    -ps               Perform a ping sweep scan
    -arp              Perform an ARP scan on the LAN
    -ptcp             Perform a TCP port scan
    -pudp             Perform a UDP port scan
osint
    -p                Scrape socials for a profile
    -w                Perform a whois lookup on a domain
proxy
    -a                Add a proxy to the list
    -t                Activate the proxy
    -f                Deactivate the proxy
    -c                Change proxy
    -s                Check proxy status
    -ls               List available proxies
get                   Fetch the content of a web page
host                  Perform a DNS lookup
domain                perform a reverse DNS lookup
clear                 Clean your terminal
quit                  Quit Doom
    """)
    
def check_connection() -> bool:
    try:
        res = requests.get("http://www.google.com")
        if res.status_code == 200:
            return True
    except:
        print("Connect to the internet to use network-related features")
        return False

def split_threads(threads, next_threads):
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    for t in next_threads:
        t.start()
        
    for t in next_threads:
        t.join()