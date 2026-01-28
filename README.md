<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/153708b1-cab5-4809-bfa3-14c36ee47931" />

# 🌐 NetScan - CLI Network Utilities Toolkit

**Simple. Fast. Unified.**

A command-line toolkit that unifies common network operations - port scanning, ping, DNS lookup, network scanning, and more. No need to remember platform-specific commands!

---

## 🎯 Why NetScan?

**Problem:** Developers constantly need to:
- Check if ports are open (is my server running?)
- Test connectivity (can I reach this host?)
- Look up IP addresses (what's the IP of this domain?)
- Find devices on network (what's on my LAN?)
- But have to remember different commands for each platform

**Solution:** NetScan provides:
- ✅ **Unified interface** - One command for all operations
- ✅ **Cross-platform** - Works on Windows, macOS, Linux
- ✅ **Fast scanning** - Concurrent port/network scans
- ✅ **Common ports** - Built-in knowledge of standard services
- ✅ **Simple syntax** - Easy to remember commands
- ✅ **Zero dependencies** - Pure Python standard library

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download
cd NetScan

# Run directly
python netscan.py --help
```

### Basic Usage

```bash
# Check if port is open
python netscan.py port example.com 80

# Scan common ports
python netscan.py ports example.com

# Ping a host
python netscan.py ping google.com

# DNS lookup
python netscan.py dns example.com
```

---

## 📖 Commands Reference

### 1. Check Single Port

```bash
# Check if port 80 is open
python netscan.py port example.com 80

# Output:
# ✅ Port 80 is OPEN (HTTP)

# Check with custom timeout
python netscan.py port example.com 443 --timeout 5
```

### 2. Scan Multiple Ports

```bash
# Scan common ports (default)
python netscan.py ports example.com

# Output:
# ✅ Open ports on example.com:
# Port      Service
# ----------------------------------------
# 80        HTTP
# 443       HTTPS
# 
# 📊 Total: 2 open port(s) found

# Scan specific port range
python netscan.py ports example.com --range 1-1000

# Scan specific ports
python netscan.py ports example.com --list 80,443,3306,5432

# Adjust performance
python netscan.py ports example.com --timeout 1 --threads 200
```

### 3. Ping Host

```bash
# Ping with default 4 packets
python netscan.py ping google.com

# Custom packet count
python netscan.py ping google.com --count 10

# Output: (platform-specific ping output)
# ✅ google.com is reachable
```

### 4. DNS Lookup

```bash
# Resolve hostname to IP
python netscan.py dns google.com

# Output:
# ✅ google.com → 172.217.164.46
```

### 5. Reverse DNS Lookup

```bash
# Resolve IP to hostname
python netscan.py rdns 8.8.8.8

# Output:
# ✅ 8.8.8.8 → dns.google
```

### 6. Show Local IP

```bash
# Get your local IP address
python netscan.py local

# Output:
# 💻 Local Network Information:
# Hostname: my-computer
# Local IP: 192.168.1.100
```

### 7. Scan Local Network

```bash
# Find all devices on your network
python netscan.py scan 192.168.1

# Output:
# 🔍 Scanning 192.168.1.1-254...
#   ✅ Found: 192.168.1.1
#   ✅ Found: 192.168.1.5
#   ✅ Found: 192.168.1.100
# 
# ✅ Found 3 active host(s):
#   192.168.1.1 (router.local)
#   192.168.1.5
#   192.168.1.100 (my-computer.local)
```

### 8. Traceroute

```bash
# Trace route to host
python netscan.py trace google.com

# Custom max hops
python netscan.py trace example.com --hops 20

# Output: (platform-specific traceroute output)
```

---

## 💡 Examples

### Example 1: Check if Web Server is Running

```bash
# Quick check
$ python netscan.py port localhost 8080
✅ Port 8080 is OPEN (HTTP Alt)

# Server is running!
```

### Example 2: Scan Server for Open Services

```bash
# Scan common ports
$ python netscan.py ports myserver.com

✅ Open ports on myserver.com:
Port      Service
----------------------------------------
22        SSH
80        HTTP
443       HTTPS
3306      MySQL

📊 Total: 4 open port(s) found
```

### Example 3: Check Network Connectivity

```bash
# Can I reach this host?
$ python netscan.py ping api.example.com

Pinging api.example.com [93.184.216.34] with 32 bytes of data:
Reply from 93.184.216.34: bytes=32 time=15ms TTL=56
Reply from 93.184.216.34: bytes=32 time=14ms TTL=56
Reply from 93.184.216.34: bytes=32 time=16ms TTL=56
Reply from 93.184.216.34: bytes=32 time=15ms TTL=56

✅ api.example.com is reachable
```

### Example 4: Find Devices on Network

```bash
# Who's on my LAN?
$ python netscan.py scan 192.168.1

🌐 Scanning network 192.168.1.0/24...
🔍 Scanning 192.168.1.1-254...
  ✅ Found: 192.168.1.1
  ✅ Found: 192.168.1.5
  ✅ Found: 192.168.1.10
  ✅ Found: 192.168.1.50

✅ Found 4 active host(s):
  192.168.1.1 (router.asus.com)
  192.168.1.5
  192.168.1.10 (raspberrypi.local)
  192.168.1.50 (laptop.local)

⏱️  Scan completed in 12.34 seconds
```

### Example 5: Debug DNS Issues

```bash
# What IP does this domain resolve to?
$ python netscan.py dns myapp.herokuapp.com
✅ myapp.herokuapp.com → 54.243.158.47

# What domain does this IP belong to?
$ python netscan.py rdns 54.243.158.47
✅ 54.243.158.47 → ec2-54-243-158-47.compute-1.amazonaws.com
```

---

## 🔧 Common Use Cases

### For Developers
- Check if local dev server is running
- Verify API endpoint connectivity
- Debug network issues
- Test firewall rules
- Find local services (databases, caches)

### For DevOps
- Quick port checks before deployment
- Verify service availability
- Network troubleshooting
- Security audits (open ports)
- Infrastructure mapping

### For Sysadmins
- Monitor network devices
- Check service status
- Troubleshoot connectivity
- Map network topology
- Verify DNS configuration

---

## 📊 Common Ports Reference

NetScan knows these common ports:

| Port | Service |
|------|---------|
| 20 | FTP Data |
| 21 | FTP Control |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 5900 | VNC |
| 6379 | Redis |
| 8080 | HTTP Alt |
| 8443 | HTTPS Alt |
| 27017 | MongoDB |

---

## ⚡ Performance Tips

### Port Scanning

```bash
# Fast scan (more threads, lower timeout)
python netscan.py ports example.com --threads 200 --timeout 0.5

# Thorough scan (fewer threads, higher timeout)
python netscan.py ports example.com --threads 50 --timeout 3
```

### Network Scanning

```bash
# Quick scan (lower timeout)
python netscan.py scan 192.168.1 --timeout 0.3

# Thorough scan (higher timeout)
python netscan.py scan 192.168.1 --timeout 1
```

---

## ❓ FAQ

### Q: Is this a network security tool?
**A:** NetScan is a diagnostic and troubleshooting tool. Only use it on networks you own or have permission to scan.

### Q: How is this different from nmap?
**A:**
- ✅ **Simpler** - NetScan has easier syntax for common tasks
- ✅ **Zero setup** - No installation, pure Python
- ✅ **Cross-platform** - Works identically on all OSes
- ❌ **Less powerful** - nmap has advanced features NetScan doesn't

Use NetScan for quick checks. Use nmap for serious security auditing.

### Q: Why is port scanning slow?
**A:** Network scanning is inherently slow (waiting for timeouts). Speed it up:
- Lower timeout: `--timeout 0.5`
- More threads: `--threads 200`
- Scan fewer ports: `--list 80,443`

### Q: Can I scan the entire internet?
**A:** Technically possible, but:
- Takes forever
- Uses lots of bandwidth
- May violate ToS/laws
- Better tools exist (Shodan, Censys)

### Q: Does this work behind a firewall?
**A:** Yes, but:
- Outbound scans usually work
- Inbound scans may be blocked
- VPN may affect results

### Q: Is this legal?
**A:** Scanning YOUR OWN networks/servers is legal. Scanning others without permission may be illegal. Use responsibly!

---

## 🔒 Responsible Use

**DO:**
- ✅ Scan your own servers
- ✅ Scan your local network
- ✅ Troubleshoot connectivity issues
- ✅ Verify your security posture

**DON'T:**
- ❌ Scan networks you don't own
- ❌ Scan without permission
- ❌ Use for malicious purposes
- ❌ Violate laws or terms of service

---

## 📄 License

MIT License - see LICENSE file for details.

**TL;DR:** Free to use, modify, and distribute. No warranty provided.

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/d220209a-afe9-4ee9-895b-ee01d56489fb" />


## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 🙏 Credits

**Built by:** FORGE (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Requested by:** Self-initiated (Tool Repair Priority 4)  
**Why:** Unified network diagnostics for Team Brain agents and BCH operations  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 2026  
**Repaired:** January 28, 2026 (added comprehensive testing, Phase 7 integration docs)

**Technology:**
- Python 3.6+
- Standard library only (socket, subprocess, concurrent.futures)
- Zero external dependencies

**Special Thanks:**
- Logan Smith for the vision of zero-dependency cross-platform tools
- Team Brain collective for testing and feedback

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Main documentation (this file) |
| [EXAMPLES.md](EXAMPLES.md) | 10 real-world usage examples |
| [CHEAT_SHEET.txt](CHEAT_SHEET.txt) | Quick reference guide |
| [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) | Team Brain integration guide |
| [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md) | 5-minute guides per agent |
| [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md) | Copy-paste code examples |

---

## 🚀 Quick Reference

```bash
# Port operations
netscan port <host> <port>                    # Check single port
netscan ports <host>                          # Scan common ports
netscan ports <host> --range 1-1000          # Scan range
netscan ports <host> --list 80,443,3306      # Scan specific

# Connectivity
netscan ping <host>                           # Ping host
netscan trace <host>                          # Traceroute

# DNS
netscan dns <host>                            # Hostname → IP
netscan rdns <ip>                             # IP → Hostname

# Network
netscan local                                 # Show local IP
netscan scan <network>                        # Scan local network
```

---

**🌐 Network troubleshooting made simple.**
