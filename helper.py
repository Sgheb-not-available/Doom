import signal
import requests
import socket

class Timeout():
    class Timeout(Exception): pass
    
    def __init__(self, sec):
        self.sec = sec
        
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0) # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()

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
        with Timeout(timeout):
            connection = s.connect((host, int(port)))
            return (host, port)
    except (Timeout.Timeout, ConnectionRefusedError, OSError):
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