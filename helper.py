import requests
import socket

from proxy import *

"""
NETWORK
"""

def check_connection() -> bool:
    try:
        res = requests.get("http://www.google.com")
        if res.status_code == 200:
            return True
    except:
        print("Connect to the internet to use network-related features")
        return False
    
def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()

def connect_tcp(host, port, timeout):
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
        
def connect_udp(host, port, attempts=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for a in range(attempts):
            code = s.connect_ex((host, int(port)))
            if code == 0:
                banner = s.recv(1024).decode()
                return code, banner
    except Exception:
        return 1
        
def connect_tcp_thread(host, open_ports, port):
    try:
        connection, banner = connect_tcp(host, port, 10)
    except TypeError:
        connection = None
                        
    if connection:
        open_ports[port] = banner
        
def connect_udp_thread(host, open_ports, port):
    try:
        code, banner = connect_udp(host, port)
    except TypeError:
        code = 1
        banner = None
        
    if code == 0:
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
    -p                Find profiles by nickname
proxy
    -a                Activate the proxy
    -d                Deactivate the proxy
    -c                Change proxy
    -s                Check proxy status
host                  Perform a DNS lookup
domain                perform a reverse DNS lookup
clear                 Clean your terminal
quit                  Quit Doom
    """)

def split_threads(threads, next_threads):
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    for t in next_threads:
        t.start()
        
    for t in next_threads:
        t.join()