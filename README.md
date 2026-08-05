# DOOM

DOOM is a modular command-line networking and OSINT toolkit written in Python. It provides a lightweight interactive shell for common reconnaissance tasks including host discovery, ARP enumeration, TCP port scanning, hostname resolution, reverse DNS lookups, and basic username reconnaissance across multiple social platforms.

> This project is intended for educational purposes and for use on systems and networks you own or are explicitly authorized to assess.

## Features

- Interactive shell
- Ping sweep of IPv4 subnets
- ARP discovery scan on local networks
- TCP port scanner
- Domain → IP resolution
- IP → Domain (reverse DNS) lookup
- Username/profile discovery across several websites
- Optional proxy support for OSINT requests
- Input validation for IP addresses, domains and scan parameters

## Requirements

- Python 3.10+
- Root/administrator privileges for ARP scanning (and recommended for some network operations)

### Python packages

Install the required dependencies:

```bash
pip install requests icmplib scapy
```

Depending on your operating system you may also need Npcap (Windows) or libpcap (Linux/macOS) for Scapy.

## Running

```bash
sudo python3 main.py
```

After startup, type:

```text
help
```

to display all available commands.

## Commands

### scanner

```
scanner -ps <network>
```

Performs a ping sweep.

Example:

```
scanner -ps 192.168.1
```

---

```
scanner -arp [cidr]
```

Performs an ARP scan of the local network.

Examples:

```
scanner -arp
scanner -arp 24
```

If omitted, `/24` is used.

---

```
scanner -ptcp <ip|domain> [port]
```

Scans TCP ports.

Examples:

```
scanner -ptcp 192.168.1.20
scanner -ptcp 192.168.1.20 80
scanner -ptcp example.com
```

When no port is specified, DOOM scans the well-known ports (1–1023).

### osint

```
osint -p <username> [-t|-f]
```

Searches for a username across several supported platforms.

Supported platforms include:

- Instagram
- Facebook
- GitHub
- Reddit
- TikTok
- Pinterest

Options:

- `-t` use a proxy
- `-f` disable proxy usage

If no option is supplied, DOOM asks whether a proxy should be used.

### host

```
host <domain>
```

Returns the IPv4 address associated with a domain.

Example:

```
host example.com
```

### domain

```
domain <ip>
```

Performs a reverse DNS lookup.

Example:

```
domain 8.8.8.8
```

### Other commands

| Command | Description |
|---------|-------------|
| help | Show available commands |
| clear | Clear the terminal |
| quit | Exit DOOM |

## Project structure

```
main.py        Interactive shell
scanner.py     Network scanning functionality
osint.py       Username reconnaissance
helper.py      Shared networking utilities
proxy.py       Proxy helper functions
```

## Notes

- Network-related commands require an active internet/network connection.
- TCP scans use multithreading for faster execution.
- ARP scans operate on the default `192.168.0.0/<cidr>` subnet.
- Invalid addresses and parameters are validated before scans begin.

## Disclaimer

Only scan infrastructure you own or have explicit permission to test. The author is not responsible for misuse of this software.
