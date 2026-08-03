import threading
from helper import *
from icmplib import multiping
from scapy.all import ARP, Ether, srp

class Scanner:
    def pingsweep(self, address):
        addresses = []
        alive = []
        for port in range(255):
            addresses.append(f"{address}.{port}")
            
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
            
    def tcp_port_scan(self, host, port):
        open_ports = []
        
        if port:
            print(f"Attempting connection to {host}:{port}")
            connection = connect_tcp(self, host, port, 10)
            if connection:
                print(f"Connection to port {port} succeeded, port is open")
            else:
                print(f"Port {port} on the {host} network is not open or protected by a firewall")
        else:
            threads = []
            for p in range(1, 1024):
                t = threading.Thread(target=connect_tcp_thread, args=(self, host, open_ports, p))
                threads.append(t)
                
            for t in threads:
                t.start()
                
            for t in threads:
                t.join()
                
            if len(open_ports) > 0:
                choice = input(f"{len(open_ports)} open ports found, do you want to list them? [y/n] ")
                if choice == "y":
                    print(open_ports)
                else:
                    print(f"All well-known ports on the {host} network are closed or protected by a firewall")