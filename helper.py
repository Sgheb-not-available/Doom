import requests
import socket
import time
import random

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
        return False

def connect_tcp(host, port, timeout) -> tuple:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(timeout)
        connection = s.connect((host, int(port)))
        return (host, port)
    except (ConnectionRefusedError, OSError):
        return None
    finally:
        s.close()
        
def connect_tcp_thread(host, open_ports, port):
    connection = connect_tcp(host, port, 10)
                        
    if connection:
        open_ports.append(port)
        
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

def split_threads(threads, next_threads):
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
        
    for t in next_threads:
        t.start()
        
    for t in next_threads:
        t.join()