# 🌐 NetScan - Usage Examples

**10 Real-World Examples with Expected Output**

Quick navigation:
- [Example 1: Basic Port Check](#example-1-basic-port-check)
- [Example 2: Scanning Common Ports](#example-2-scanning-common-ports)
- [Example 3: Custom Port Range Scan](#example-3-custom-port-range-scan)
- [Example 4: Testing Connectivity with Ping](#example-4-testing-connectivity-with-ping)
- [Example 5: DNS Lookup and Resolution](#example-5-dns-lookup-and-resolution)
- [Example 6: Network Discovery](#example-6-network-discovery)
- [Example 7: Server Health Check](#example-7-server-health-check)
- [Example 8: Debugging Connection Issues](#example-8-debugging-connection-issues)
- [Example 9: Python API Usage](#example-9-python-api-usage)
- [Example 10: Full DevOps Workflow](#example-10-full-devops-workflow)

---

## Example 1: Basic Port Check

**Scenario:** You want to check if your local development server is running on port 8080.

**Steps:**

```bash
# Check if port 8080 is open on localhost
python netscan.py port localhost 8080
```

**Expected Output (Server Running):**

```
🔍 Checking localhost:8080...
✅ Port 8080 is OPEN (HTTP Alt)
```

**Expected Output (Server Not Running):**

```
🔍 Checking localhost:8080...
❌ Port 8080 is CLOSED or FILTERED
```

**What You Learned:**
- Basic syntax: `netscan port <host> <port>`
- Quick way to verify if a service is listening
- NetScan knows common port names (HTTP Alt = 8080)

---

## Example 2: Scanning Common Ports

**Scenario:** You want to see what services are running on a remote server.

**Steps:**

```bash
# Scan common ports on a server
python netscan.py ports myserver.example.com

# Or with shorter timeout for faster scan
python netscan.py ports myserver.example.com --timeout 1
```

**Expected Output:**

```
🔍 Scanning 19 port(s) on myserver.example.com...
⏱️  Timeout: 2.0s | Threads: 100

✅ Open ports on myserver.example.com:

Port      Service
----------------------------------------
22        SSH
80        HTTP
443       HTTPS
3306      MySQL

📊 Total: 4 open port(s) found

⏱️  Scan completed in 0.45 seconds
```

**What You Learned:**
- Default scan checks 19 common ports
- Results show port numbers and service names
- Concurrent scanning is fast (< 1 second typically)

---

## Example 3: Custom Port Range Scan

**Scenario:** You need to scan a specific range of ports for security audit.

**Steps:**

```bash
# Scan ports 1-1000
python netscan.py ports target.example.com --range 1-1000

# Scan specific ports only
python netscan.py ports target.example.com --list 22,80,443,3000,5000,8080

# High-performance scan with more threads
python netscan.py ports target.example.com --range 1-65535 --timeout 0.5 --threads 200
```

**Expected Output (Range Scan):**

```
🔍 Scanning 1000 port(s) on target.example.com...
⏱️  Timeout: 2.0s | Threads: 100

✅ Open ports on target.example.com:

Port      Service
----------------------------------------
22        SSH
80        HTTP
443       HTTPS
3000      Unknown

📊 Total: 4 open port(s) found

⏱️  Scan completed in 12.34 seconds
```

**What You Learned:**
- Use `--range` for port ranges (e.g., 1-1000)
- Use `--list` for specific ports
- Adjust `--threads` and `--timeout` for performance

---

## Example 4: Testing Connectivity with Ping

**Scenario:** You want to verify network connectivity to a host.

**Steps:**

```bash
# Basic ping (4 packets)
python netscan.py ping google.com

# More packets for reliability test
python netscan.py ping api.example.com --count 10
```

**Expected Output:**

```
🏓 Pinging google.com...

Pinging google.com [172.217.164.46] with 32 bytes of data:
Reply from 172.217.164.46: bytes=32 time=12ms TTL=118
Reply from 172.217.164.46: bytes=32 time=11ms TTL=118
Reply from 172.217.164.46: bytes=32 time=13ms TTL=118
Reply from 172.217.164.46: bytes=32 time=11ms TTL=118

Ping statistics for 172.217.164.46:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 11ms, Maximum = 13ms, Average = 11ms

✅ google.com is reachable
```

**What You Learned:**
- Ping uses platform-native commands
- Output format matches your OS (Windows/Linux/macOS)
- Clear success/failure indication at the end

---

## Example 5: DNS Lookup and Resolution

**Scenario:** You need to resolve hostnames to IPs and vice versa for debugging.

**Steps:**

```bash
# DNS lookup (hostname to IP)
python netscan.py dns api.github.com

# Reverse DNS (IP to hostname)
python netscan.py rdns 8.8.8.8

# Get your local IP
python netscan.py local
```

**Expected Output (DNS Lookup):**

```
🔍 Resolving api.github.com...
✅ api.github.com → 140.82.112.6
```

**Expected Output (Reverse DNS):**

```
🔍 Reverse resolving 8.8.8.8...
✅ 8.8.8.8 → dns.google
```

**Expected Output (Local IP):**

```
💻 Local Network Information:

Hostname: my-computer
Local IP: 192.168.1.100
```

**What You Learned:**
- `dns` resolves hostnames to IPs
- `rdns` does reverse lookup (IP to hostname)
- `local` shows your machine's network info

---

## Example 6: Network Discovery

**Scenario:** You want to find all active devices on your local network.

**Steps:**

```bash
# Scan local network (use your network prefix)
python netscan.py scan 192.168.1

# Faster scan with lower timeout
python netscan.py scan 192.168.1 --timeout 0.3
```

**Expected Output:**

```
🌐 Scanning network 192.168.1.0/24...

🔍 Scanning 192.168.1.1-254...
  ✅ Found: 192.168.1.1
  ✅ Found: 192.168.1.5
  ✅ Found: 192.168.1.10
  ✅ Found: 192.168.1.50
  ✅ Found: 192.168.1.100

✅ Found 5 active host(s):

  192.168.1.1 (router.local)
  192.168.1.5
  192.168.1.10 (raspberrypi.local)
  192.168.1.50 (laptop.local)
  192.168.1.100 (desktop.local)

⏱️  Scan completed in 15.67 seconds
```

**What You Learned:**
- Network scan finds devices by checking common ports
- Automatically resolves hostnames when possible
- Use first 3 octets of your network (e.g., 192.168.1)

---

## Example 7: Server Health Check

**Scenario:** You want a quick health check of your production servers.

**Steps:**

```bash
# Check web server
python netscan.py port webserver.example.com 80
python netscan.py port webserver.example.com 443

# Check database
python netscan.py port dbserver.example.com 3306

# Check SSH access
python netscan.py port jumpbox.example.com 22
```

**Expected Output (All Healthy):**

```
🔍 Checking webserver.example.com:80...
✅ Port 80 is OPEN (HTTP)

🔍 Checking webserver.example.com:443...
✅ Port 443 is OPEN (HTTPS)

🔍 Checking dbserver.example.com:3306...
✅ Port 3306 is OPEN (MySQL)

🔍 Checking jumpbox.example.com:22...
✅ Port 22 is OPEN (SSH)
```

**What You Learned:**
- Quick per-service health checks
- Useful for monitoring scripts
- Can be combined into shell scripts or automation

---

## Example 8: Debugging Connection Issues

**Scenario:** Your application can't connect to an API. You need to diagnose the issue.

**Steps:**

```bash
# Step 1: Check DNS resolution
python netscan.py dns api.example.com

# Step 2: Check connectivity
python netscan.py ping api.example.com

# Step 3: Check if port is open
python netscan.py port api.example.com 443

# Step 4: Trace the route
python netscan.py trace api.example.com
```

**Expected Output (DNS Issue):**

```
🔍 Resolving api.example.com...
❌ Could not resolve api.example.com
```

**Expected Output (Port Blocked):**

```
🔍 Resolving api.example.com...
✅ api.example.com → 93.184.216.34

🏓 Pinging api.example.com...
✅ api.example.com is reachable

🔍 Checking api.example.com:443...
❌ Port 443 is CLOSED or FILTERED
```

**Diagnosis:** Host is reachable but firewall is blocking HTTPS.

**What You Learned:**
- Systematic approach to network debugging
- DNS → Ping → Port → Traceroute
- Quickly identify where the problem is

---

## Example 9: Python API Usage

**Scenario:** You want to integrate NetScan into your Python application.

**Steps:**

```python
#!/usr/bin/env python3
"""Example: Using NetScan in Python code."""

from netscan import NetScan, COMMON_PORTS

# Initialize
ns = NetScan()

# Example 1: Check single port
is_open = ns.scan_port("google.com", 443)
print(f"HTTPS open: {is_open}")  # True

# Example 2: Scan multiple ports
results = ns.scan_ports("myserver.com", [22, 80, 443, 3306])
open_ports = [port for port, is_open in results.items() if is_open]
print(f"Open ports: {open_ports}")  # [22, 80, 443]

# Example 3: DNS operations
ip = ns.dns_lookup("github.com")
print(f"GitHub IP: {ip}")  # 140.82.112.4

hostname = ns.reverse_dns("8.8.8.8")
print(f"8.8.8.8 is: {hostname}")  # dns.google

# Example 4: Get local network info
local_ip = ns.get_local_ip()
print(f"My IP: {local_ip}")  # 192.168.1.100

# Example 5: Ping with result
success, output = ns.ping("google.com", count=2)
print(f"Google reachable: {success}")  # True

# Example 6: Check server health
def check_server_health(host):
    """Check if a server is healthy."""
    ns = NetScan()
    
    # Check common web ports
    results = ns.scan_ports(host, [80, 443])
    
    web_healthy = results.get(80, False) or results.get(443, False)
    
    # Check SSH
    ssh_healthy = ns.scan_port(host, 22)
    
    return {
        "host": host,
        "web": web_healthy,
        "ssh": ssh_healthy,
        "ip": ns.dns_lookup(host)
    }

health = check_server_health("myserver.example.com")
print(f"Server health: {health}")
```

**Expected Output:**

```
HTTPS open: True
Open ports: [22, 80, 443]
GitHub IP: 140.82.112.4
8.8.8.8 is: dns.google
My IP: 192.168.1.100
Google reachable: True
Server health: {'host': 'myserver.example.com', 'web': True, 'ssh': True, 'ip': '93.184.216.34'}
```

**What You Learned:**
- All CLI features available as Python API
- Easy integration into automation scripts
- Returns data structures (bool, dict, str) for programmatic use

---

## Example 10: Full DevOps Workflow

**Scenario:** You're deploying to production and need to verify infrastructure.

**Steps:**

```bash
#!/bin/bash
# pre-deploy-check.sh - Run before deployment

echo "=== Pre-Deployment Infrastructure Check ==="

# Check load balancer
echo -e "\n[1/5] Checking load balancer..."
python netscan.py port lb.example.com 443

# Check web servers
echo -e "\n[2/5] Checking web servers..."
python netscan.py port web1.example.com 80
python netscan.py port web2.example.com 80

# Check database
echo -e "\n[3/5] Checking database..."
python netscan.py port db.example.com 5432

# Check cache
echo -e "\n[4/5] Checking Redis cache..."
python netscan.py port cache.example.com 6379

# Check message queue
echo -e "\n[5/5] Checking RabbitMQ..."
python netscan.py port mq.example.com 5672

echo -e "\n=== All checks complete ==="
```

**Expected Output:**

```
=== Pre-Deployment Infrastructure Check ===

[1/5] Checking load balancer...
🔍 Checking lb.example.com:443...
✅ Port 443 is OPEN (HTTPS)

[2/5] Checking web servers...
🔍 Checking web1.example.com:80...
✅ Port 80 is OPEN (HTTP)
🔍 Checking web2.example.com:80...
✅ Port 80 is OPEN (HTTP)

[3/5] Checking database...
🔍 Checking db.example.com:5432...
✅ Port 5432 is OPEN (PostgreSQL)

[4/5] Checking Redis cache...
🔍 Checking cache.example.com:6379...
✅ Port 6379 is OPEN (Redis)

[5/5] Checking RabbitMQ...
🔍 Checking mq.example.com:5672...
✅ Port 5672 is OPEN (Unknown)

=== All checks complete ===
```

**What You Learned:**
- NetScan integrates well with shell scripts
- Can be part of CI/CD pipelines
- Quick infrastructure verification before deployment

---

## 📋 Command Quick Reference

| Command | Description |
|---------|-------------|
| `port <host> <port>` | Check single port |
| `ports <host>` | Scan common ports |
| `ports <host> --range 1-1000` | Scan port range |
| `ports <host> --list 80,443` | Scan specific ports |
| `ping <host>` | Ping host |
| `dns <host>` | DNS lookup |
| `rdns <ip>` | Reverse DNS |
| `local` | Show local IP |
| `scan <network>` | Scan local network |
| `trace <host>` | Traceroute |

---

## 🔧 Performance Tips

1. **Faster scans:** Use `--timeout 0.5 --threads 200`
2. **Specific ports:** Use `--list` instead of ranges
3. **Network scan:** Lower timeout with `--timeout 0.3`
4. **Large ranges:** Increase threads with `--threads 200`

---

**Built with ❤️ by Team Brain for Logan Smith / Metaphy LLC**
