import os
import re

from helper import *
from scanner import Scanner
from osint import Osint

class Main:
    def __init__(self):
        print_doom()
        self.shell()
    
    def shell(self):
        proxy = None
        
        d_octate = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)"
        d_ipv4 = rf"^{d_octate}\.{d_octate}\.{d_octate}\.{d_octate}$"
        d_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))*\.[A-Za-z]{2,}$"
        
        print("\nType 'help' to list available commands")
        
        while True:
            try:
                command = input(f"\n> ").strip().split()
                    
                if not command:
                    continue

                cmd = command[0].lower()
                args = command[1:]

                if cmd == "help":
                    print_cmds()
                elif cmd == "scanner":
                    if check_connection():
                        if not args:
                            print("Use: scanner [scan type] [address / range]")
                        else:
                            scan_type = args[0]
                            address = args[1] if len(args) > 1 else None
                            port = args[2] if len(args) > 2 else None

                            if scan_type == "-ps":
                                if address and bool(re.match(rf"^{d_octate}\.{d_octate}\.{d_octate}$", address)):
                                    Scanner.pingsweep(self, address)
                                else:
                                    print("Address should be written like this: [0-255].[0-255].[0-255]")
                            elif scan_type == "-arp":
                                if address:
                                    pattern = r'^(1[0-9]|2[0-4]|[1-9])$'
                                    if bool(re.match(pattern, address)): 
                                        Scanner.arp_scan(self, address)
                                    else:
                                        print("Range should be between 1 and 24") # ?
                                else:
                                    Scanner.arp_scan(self, "24")
                            elif scan_type == "-ptcp":             
                                if address:
                                    if bool(re.match(d_ipv4, address)):
                                        Scanner.tcp_port_scan(self, address, port)
                                    elif bool(re.match(d_pattern, address)):
                                        host = get_host(address)
                                        if host:
                                            Scanner.tcp_port_scan(self, host, port)
                                        else:
                                            print(f"{address} is not a registered domain")
                                    else:
                                        print("Address should be written like this: [0-255].[0-255].[0-255].[0-255] or be a domain name")
                                else:
                                    print("You must provide an address in order for the tcp port scan to happen")
                            elif scan_type == "-pudp":
                                if address:
                                    if bool(re.match(d_ipv4, address)):
                                        Scanner.udp_port_scan(self, address, port)
                                    elif bool(re.match(d_pattern, address)):
                                        host = get_host(address)
                                        if host:
                                            Scanner.udp_port_scan(self, host, port)
                                        else:
                                            print(f"{address} is not a registered domain")
                                    else:
                                        print("Address should be written like this: [0-255].[0-255].[0-255].[0-255] or be a domain name")
                                else:
                                    print("You must provide an address in order for the udp port scan to happen")                                
                            else:
                                print(f"Invalid argument '{args[0]}'. Type help to list available commands")
                elif cmd == "osint":
                    if check_connection():
                        if not args:
                            print("Use: osint [search type] [name]")
                        else:
                            search_type = args[0]
                            name = args[1]
                            
                            if search_type == "-p":
                                if not proxy:
                                    choice = input("Please note that scraping might be illegal on some social media platforms, do you want to use a proxy? [y/n] ")
                                    if choice == "y":
                                        proxy = get_proxy(proxy)
                                
                                Osint.profile_scan(self, name, proxy)
                elif cmd == "proxy":
                    if check_connection():
                        if not args:
                            print("Use: proxy [action]")
                        else:
                            action = args[0]
                            if action == "-a":
                                if proxy:
                                    print("proxy is already active")
                                else:
                                    proxy = get_proxy(proxy)
                            elif action == "-d":
                                if proxy:
                                    proxy = None
                                    print("Deactivated proxy")
                                else:
                                    print("proxy is already deactivated")
                            elif action == "-c":
                                if proxy:
                                    proxy = get_proxy(proxy)
                                else:
                                    print("No active proxy to change")
                            elif action == "-s":
                                if proxy:
                                    print(f"Proxy is active, current proxy: {proxy["http"]}")
                                else:
                                    print("No active proxy")
                            else:
                                print(f"'{action}' is not a valid action, type 'help' to list available commands")
                elif cmd == "host":
                    if check_connection():
                        if not args:
                            print("Use: host [domain]")
                        else:
                            domain = args[0]
                            
                            if bool(re.match(d_pattern, domain)):
                                host = get_host(domain)
                                if host:
                                    print(f"{domain} is hosted on {host}")
                                else:
                                    print(f"{domain} does not exist")
                            else:
                                print(f"{domain} is not a domain name")
                elif cmd == "domain":
                    if check_connection():
                        if not args:
                            print("Use: domain [ip]")
                        else:
                            address = args[0]

                            if bool(re.match(d_ipv4, address)):
                                domain = get_domain(address)
                                if domain:
                                    print(f"{address} is hosting {domain}")
                                else:
                                    print(f"{address} does not exist or isn't hosting a domain")
                            else:
                                print("Address should be written like this: [0-255].[0-255].[0-255].[0-255]")
                elif cmd == "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    print_doom()
                elif cmd == "quit":
                    print("Closing Doom...")
                    exit()
                else:
                    print(f"Command '{cmd}' not found")
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected, exiting program...")
                exit()
            
if __name__ == "__main__":
    Main()