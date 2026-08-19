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
                    choice = input(f"\nPort 80 is open, do you want to grab the contents of {get_domain(host)}, which is hosted on this ip? [y/n] ")
                    if choice == "y":
                        get_content(host, proxy)
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
                            choice = input(f"\nPort 80 is open, do you want to grab the contents of {get_domain(host)}, which is hosted on this ip? [y/n] ")
                            if choice == "y":
                                get_content(host, proxy)
            else:
                print(f"All well-known ports on the {host} subnet are closed or protected by a firewall")
                
    def udp_port_scan(self, host, port):
        open_ports = {}
        start = time.time()
        
        if port:
            print(f"Attempting connection to {host}:{port}")
            connection = probe_udp(host, port)
            if connection:
                print(f"Connection to port {port} succeeded, port is open")
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
            else:
                print(f"Couldn't connect to any well-known port on the {host} subnet, try a tcp scan if you think this was caused by packet loss")