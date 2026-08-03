# DOOM

A simple interactive command-line network scanning tool. DOOM gives you a small shell where you can run ping sweeps, ARP scans, and TCP port scans.

## Requirements

- Python 3
- An internet/network connection (required for the `scanner` commands)

## Getting Started

Run the program from your terminal:

```
sudo python3 main.py
```

You'll see the DOOM banner, followed by a prompt:

```
> 
```

Type `help` at any time to see the list of available commands.

## Commands

### `help`
Lists all available commands and their usage.

### `clear`
Clears your terminal screen.

### `exit`
Quits DOOM.

### `scanner`
Runs a network scan. Requires an active network connection — if you're not connected, DOOM will tell you to connect first.

Usage:

```
scanner [scan type] [address / range] [port]
```

There are three scan types:

#### `-ps` — Ping Sweep
Checks which hosts on a given subnet are online by pinging each address in the range.

**Format:** the first three octets of an IP address (no trailing dot or last octet), e.g. `192.168.1`

```
> scanner -ps 192.168.1
```

If the address isn't formatted correctly (each octate must be a number from 0–255), you'll get an error message reminding you of the correct format.

#### `-arp` — ARP Scan
Scans your local network using ARP requests to discover connected devices. This is useful for quickly identifying devices on your LAN (IP address, MAC address, etc.).

**Format:** a number representing the subnet size in CIDR notation, between `1` and `24`.

```
> scanner -arp 24
```

If you don't provide a range, DOOM defaults to `24` (equivalent to a typical `/24` home network).

```
> scanner -arp
```

#### `-ptcp` — TCP Port Scan
Scans a target IP address for open TCP ports.

**Format:** a full IPv4 address, e.g. `192.168.1.10`. You can optionally specify a port (or port range, depending on how `scanner.py` implements it) as a third argument.

```
> scanner -ptcp 192.168.1.10
> scanner -ptcp 192.168.1.10 80
```

If the IP address isn't valid, DOOM will remind you of the correct format.

## Notes on Usage

- All `scanner` commands check for an active internet connection before running. If you're offline, you'll see: `Connect to the internet to use network-related features`.
- Address validation is done with regular expressions, so scans won't run unless the address format matches what's expected — read the error message for the exact format required.
- Running `scanner` with no arguments will remind you of the correct syntax:
  ```
  Use: scanner [scan type] [address / range]
  ```

## Quick Reference

| Command          | Description                        |
|------------------|-------------------------------------|
| `help`           | Show available commands             |
| `scanner -ps`    | Ping sweep a subnet                 |
| `scanner -arp`   | ARP scan the LAN (default range 24) |
| `scanner -ptcp`  | TCP port scan a specific IP         |
| `clear`          | Clear the terminal                  |
| `exit`           | Quit DOOM                           |

## Disclaimer

Only scan networks and devices you own or have explicit permission to test. Unauthorized network scanning may be illegal in your jurisdiction.