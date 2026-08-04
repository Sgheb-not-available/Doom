import os
import re

from helper import *
from scanner import Scanner
from osint import Osint

class Main:
    def __init__(self):
        print(r"""
██████╗  ██████╗  ██████╗ ███╗   ███╗
██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║  ██║██║   ██║██║   ██║██╔████╔██║
██║  ██║██║   ██║██║   ██║██║╚██╔╝██║
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
        """)
        
        self.shell()
    
    def shell(self):
        print("\nType 'help' to list available commands")
        
        while True:
            command = input(f"\n> ").strip().split()
                
            if not command:
                continue

            cmd = command[0].lower()
            args = command[1:]

            if cmd == "help":
                print("""
Available commands:
scanner
    -ps               Perform a ping sweep scan
    -arp              Perform an ARP scan on the LAN
    -ptcp             Perform a TCP port scan
osint
    -p                Find profiles by nickname
host                  Get host from domain name
domain                Get domain name from host
clear                 Clean your terminal
quit                  Quit Doom
                """)
            elif cmd == "scanner":
                if check_connection(self):
                    if not args:
                        print("Use: scanner [scan type] [address / range]")
                    else:
                        scan_type = args[0]
                        address = args[1] if len(args) > 1 else None
                        port = args[2] if len(args) > 2 else None

                        if scan_type == "-ps":
                            pattern = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)"
                            
                            if address and bool(re.match(rf"^{pattern}\.{pattern}\.{pattern}$", address)):
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
                            pattern = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)"
                            d_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))*\.[A-Za-z]{2,}$"
                            
                            if address:
                                if bool(re.match(rf"^{pattern}\.{pattern}\.{pattern}\.{pattern}$", address)):
                                    Scanner.tcp_port_scan(self, address, port)
                                elif bool(re.match(d_pattern, address)):
                                    host = get_host(self, address)
                                    Scanner.tcp_port_scan(self, host, port)
                                else:
                                    print("Address should be written like this: [0-255].[0-255].[0-255].[0-255] or be a domain name")
                            else:
                                print("You must provide an address in order for the tcp port scan to happen")
                        else:
                            print(f"Invalid argument '{args[0]}'. Type help to list available commands")
                else:
                    print("Connect to the internet to use network-related features")
            elif cmd == "osint":
                if check_connection(self):
                    if not args:
                        print("Use: osint [search type] [name]")
                    else:
                        search_type = args[0]
                        name = args[1]
                        
                        if search_type == "-p":
                            Osint.profile_scan(self, name)
                else:
                    print("Connect to the internet to use network-related features")
            elif cmd == "host":
                if check_connection(self):
                    if not args:
                        print("Use: host [domain]")
                    else:
                        domain = args[0]
                        
                        d_pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))*\.[A-Za-z]{2,}$"
                        if bool(re.match(d_pattern, domain)):
                            host = get_host(self, domain)
                            if host:
                                print(f"{domain} is hosted on {host}")
                            else:
                                print(f"{domain} does not exist")
                        else:
                            print(f"{domain} is not a domain name")
                else:
                    print("Connect to the internet to use network-related features")
            elif cmd == "domain":
                if check_connection(self):
                    if not args:
                        print("Use: domain [ip]")
                    else:
                        address = args[0]
                        
                        pattern = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)"
                        if bool(re.match(rf"^{pattern}\.{pattern}\.{pattern}\.{pattern}$", address)):
                            domain = get_domain(self, address)
                            if domain:
                                print(f"{address} is hosting {domain}")
                            else:
                                print(f"{address} does not exist or isn't hosting a domain")
                        else:
                            print("Address should be written like this: [0-255].[0-255].[0-255].[0-255]")
                else:
                    print("Connect to the internet to use network-related features")
            elif cmd == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                
                print(r"""
██████╗  ██████╗  ██████╗ ███╗   ███╗
██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║  ██║██║   ██║██║   ██║██╔████╔██║
██║  ██║██║   ██║██║   ██║██║╚██╔╝██║
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
                """)
            elif cmd == "quit":
                print("Closing Doom...")
                exit()
            else:
                print(f"Command '{cmd}' not found")
            
if __name__ == "__main__":
    Main()