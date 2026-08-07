# DOOM

**DOOM** is a modular command-line networking and OSINT toolkit written in Python. It provides a lightweight interactive shell for reconnaissance tasks on networks and systems you own or are authorized to test — host discovery, ARP enumeration, TCP/UDP port scanning, DNS resolution, and username lookups across a handful of social platforms.

> ⚠️ **Educational use only.** Only run DOOM against systems and networks you own or have explicit written authorization to test. See [Disclaimer](#disclaimer).

```
██████╗  ██████╗  ██████╗ ███╗   ███╗
██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║  ██║██║   ██║██║   ██║██╔████╔██║
██║  ██║██║   ██║██║   ██║██║╚██╔╝██║
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
```

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Project structure](#project-structure)
- [Notes](#notes)
- [Disclaimer](#disclaimer)

## Features

| Category | Capability |
|---|---|
| Discovery | Ping sweep across an IPv4 /24, ARP scan on the local subnet |
| Port scanning | Multithreaded TCP and UDP port scans, full range or a single port |
| DNS | Domain → IP resolution, IP → domain reverse lookup |
| OSINT | Username/profile lookup across Instagram, Facebook, GitHub, Reddit, TikTok, and Pinterest |
| Networking | Optional proxy rotation for OSINT requests, connectivity check before any network command |
| Shell | Simple input validation for IPs, domains, and CIDR ranges; `clear` and `quit` built in |

## Requirements

- Python 3.10+
- Root/administrator privileges (required for ARP scanning, recommended for port scanning)

### Python packages

```bash
pip install requests icmplib scapy
```

Scapy also needs a packet-capture backend: **Npcap** on Windows, or **libpcap** on Linux/macOS.

## Installation

```bash
git clone <repo-url>
cd doom
pip install requests icmplib scapy
```

## Usage

```bash
sudo python3 main.py
```

Once the shell starts, type `help` to list all available commands:

```
> help

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
```

Every network-dependent command first checks that you have an active internet connection, and prints a message rather than crashing if you don't.

## Commands

### `scanner -ps <network>`

Ping sweeps a `/24`-style range, e.g. `192.168.1`, and reports which of the 255 hosts respond.

```
scanner -ps 192.168.1
```

### `scanner -arp [cidr]`

ARP-scans the local subnet. DOOM detects the machine's active local IPv4 address and combines it with the given CIDR prefix to pick the subnet, so it always targets the network you're actually connected to rather than a hardcoded range. `cidr` must be between 1 and 24; it defaults to 24 if omitted.

```
scanner -arp
scanner -arp 24
scanner -arp 16
```

### `scanner -ptcp <ip|domain> [port]`

TCP port scan against an IP address or a domain (domains are resolved automatically). With no port given, scans the well-known range 1–1023 using multiple threads; with a port given, checks just that one.

```
scanner -ptcp 192.168.1.20
scanner -ptcp 192.168.1.20 80
scanner -ptcp example.com
```

### `scanner -pudp <ip|domain> [port]`

UDP port scan, same address/port rules as `-ptcp`.

```
scanner -pudp 192.168.1.20
scanner -pudp example.com 53
```

### `osint -p <username>`

Checks whether a given username/handle exists on Instagram, Facebook, GitHub, Reddit, TikTok, and Pinterest, and prints a per-platform result summary. If no proxy is active yet, DOOM warns that scraping some of these platforms may violate their terms of service and asks whether to route the request through a proxy. Run `proxy -a` beforehand to skip that prompt.

```
osint -p someusername
```

### `proxy <action>`

Controls the proxy used for OSINT requests.

| Action | Description |
|---|---|
| `-a` | Activate a proxy (picks a working one from the built-in list) |
| `-d` | Deactivate the current proxy |
| `-c` | Change to a different proxy |
| `-s` | Show current proxy status |

```
proxy -a
proxy -s
proxy -d
```

### `host <domain>`

Resolves a domain name to its IPv4 address.

```
host example.com
```

### `domain <ip>`

Reverse-resolves an IPv4 address to a hostname.

```
domain 8.8.8.8
```

### Other commands

| Command | Description |
|---|---|
| `help` | Show available commands |
| `clear` | Clear the terminal |
| `quit` | Exit DOOM |

## Project structure

```
main.py        Interactive shell and command dispatch
scanner.py     Ping sweep, ARP scan, TCP/UDP port scanning
osint.py       Username/profile lookup across social platforms
proxy.py       Proxy selection and rotation
helper.py      Shared networking utilities, banner and help text
```

## Notes

- Network commands require an active internet connection, checked before each run.
- TCP and UDP scans are multithreaded for speed.
- ARP scans target the subnet derived from the host's active local IP and the given CIDR prefix (default `/24`), not a fixed address range.
- Addresses, domains, and scan parameters are validated before a scan starts.

## Disclaimer

Only scan infrastructure you own or have explicit permission to test. The author is not responsible for misuse of this software.