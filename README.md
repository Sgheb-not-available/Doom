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
osint -p <username>
```

Searches for a username across several supported platforms.

Supported platforms include:

- Instagram
- Facebook
- GitHub
- Reddit
- TikTok
- Pinterest

If no proxy is currently active, DOOM asks whether one should be used for the request (`y`/`n`). Use `proxy -a` beforehand to skip this prompt.

### proxy

```
proxy <action>
```

Manages the proxy used for OSINT requests.

| Action | Description |
|--------|-------------|
| `-a` | Activate a proxy (picks a working one from the proxy list) |
| `-d` | Deactivate the current proxy |
| `-c` | Change to a different proxy |
| `-s` | Show current proxy status |

Example:

```
proxy -a
proxy -s
proxy -d
```

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
scanner.py     Network scanning functionality (ping sweep, ARP scan, TCP port scan)
osint.py       Username reconnaissance across social platforms
helper.py      Shared networking utilities, banner/help text
proxy.py       Proxy selection and rotation helper
```

## Notes

- Network-related commands require an active internet/network connection.
- TCP scans use multithreading for faster execution.
- ARP scans operate on the default `192.168.0.0/<cidr>` subnet.
- Invalid addresses and parameters are validated before scans begin.

## Disclaimer

Only scan infrastructure you own or have explicit permission to test. The author is not responsible for misuse of this software.