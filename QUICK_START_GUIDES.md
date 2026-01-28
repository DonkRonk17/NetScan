# 🌐 NetScan - Quick Start Guides

**5-Minute Guides for Every Team Brain Agent**

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#-forge-quick-start)
- [Atlas (Executor)](#-atlas-quick-start)
- [Clio (Linux Agent)](#-clio-quick-start)
- [Nexus (Multi-Platform)](#-nexus-quick-start)
- [Bolt (Free Executor)](#-bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use NetScan for infrastructure verification and deployment reviews

### Step 1: Installation Check

```bash
# Navigate to NetScan
cd C:\Users\logan\OneDrive\Documents\AutoProjects\NetScan

# Verify NetScan is available
python netscan.py --help

# Expected: Help text with all commands
```

### Step 2: First Use - Infrastructure Verification

```bash
# Quick infrastructure check before deployment review
python netscan.py ports api.beaconhq.local --list 80,443,5000

# Check database connectivity
python netscan.py port db.beaconhq.local 5432

# Verify all components are up
python netscan.py ping loadbalancer.beaconhq.local
```

### Step 3: Integration with Forge Workflows

**Use Case 1: Pre-Deployment Checklist**

```python
# Forge session: Verify infrastructure before approving deployment
from netscan import NetScan

def pre_deployment_check():
    """Run before approving any deployment."""
    ns = NetScan()
    
    services = {
        "API": ("api.beaconhq.local", 5000),
        "Database": ("db.beaconhq.local", 5432),
        "Cache": ("cache.beaconhq.local", 6379),
    }
    
    all_ok = True
    for name, (host, port) in services.items():
        status = ns.scan_port(host, port)
        print(f"  {'[OK]' if status else '[X]'} {name}: {host}:{port}")
        all_ok = all_ok and status
    
    return all_ok

if pre_deployment_check():
    print("\n[OK] Approved for deployment")
else:
    print("\n[X] Deployment blocked - fix issues first")
```

**Use Case 2: Debug Connection Issues from Other Agents**

```bash
# When another agent reports connection issues
python netscan.py dns api.example.com              # Check DNS
python netscan.py ping api.example.com             # Check reachability
python netscan.py port api.example.com 443         # Check port
python netscan.py trace api.example.com            # Trace route
```

### Step 4: Common Forge Commands

```bash
# Pre-deployment verification
python netscan.py ports prod.example.com --list 80,443,5000,5432

# Quick health check
python netscan.py port api.example.com 443

# Network topology discovery
python netscan.py scan 192.168.1 --timeout 0.5
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 7 (Server Health Check)
3. Add infrastructure checks to your deployment review workflow

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use NetScan for debugging during tool development

### Step 1: Installation Check

```bash
# Verify installation
cd C:\Users\logan\OneDrive\Documents\AutoProjects\NetScan
python -c "from netscan import NetScan; print('OK')"
```

### Step 2: First Use - Debug API Connectivity

```python
# In your Atlas session
from netscan import NetScan

ns = NetScan()

# Check if API is reachable before integration
api_host = "api.github.com"

print(f"DNS: {ns.dns_lookup(api_host)}")
print(f"Port 443: {ns.scan_port(api_host, 443)}")

success, output = ns.ping(api_host, count=2)
print(f"Ping: {'OK' if success else 'FAILED'}")
```

### Step 3: Integration with Build Workflows

**During Tool Creation:**

```python
# Example: Verify external dependencies before building
from netscan import NetScan

def check_build_dependencies():
    """Check all external APIs needed for build."""
    ns = NetScan()
    
    dependencies = [
        ("GitHub API", "api.github.com", 443),
        ("PyPI", "pypi.org", 443),
        ("NPM Registry", "registry.npmjs.org", 443),
    ]
    
    for name, host, port in dependencies:
        is_reachable = ns.scan_port(host, port)
        status = "[OK]" if is_reachable else "[X]"
        print(f"{status} {name}: {host}:{port}")

check_build_dependencies()
```

**Error Debugging:**

```bash
# When tests fail with connection errors
python netscan.py dns api.example.com          # DNS issue?
python netscan.py port api.example.com 443     # Port blocked?
python netscan.py trace api.example.com        # Network path issue?
```

### Step 4: Common Atlas Commands

```bash
# Test endpoint before API integration
python netscan.py port api.github.com 443

# Check local development servers
python netscan.py port localhost 8080
python netscan.py port localhost 5000
python netscan.py port localhost 3000

# Debug DNS issues
python netscan.py dns api.example.com

# Trace route for latency issues
python netscan.py trace api.example.com
```

### Next Steps for Atlas

1. Integrate into Holy Grail automation
2. Add to tool build checklist
3. Use for every new tool build that requires network

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use NetScan for Linux server administration

### Step 1: Linux Installation

```bash
# Clone from GitHub (if not already present)
git clone https://github.com/DonkRonk17/NetScan.git
cd NetScan

# Or navigate to existing installation
cd /path/to/AutoProjects/NetScan

# Verify
python3 netscan.py --version
```

### Step 2: First Use - Server Diagnostics

```bash
# Check local services
python3 netscan.py port localhost 22      # SSH
python3 netscan.py port localhost 80      # Nginx/Apache
python3 netscan.py port localhost 443     # HTTPS
python3 netscan.py port localhost 5432    # PostgreSQL

# Get local network info
python3 netscan.py local
```

### Step 3: Integration with Clio Workflows

**Use Case: Server Health Script**

```bash
#!/bin/bash
# clio_server_check.sh - Run periodically via cron

echo "=== Server Health Check ==="
echo "Time: $(date)"
echo ""

# Check critical services
echo "Services:"
python3 netscan.py port localhost 22 2>/dev/null | tail -1
python3 netscan.py port localhost 80 2>/dev/null | tail -1
python3 netscan.py port localhost 5432 2>/dev/null | tail -1

# Check external connectivity
echo ""
echo "External:"
python3 netscan.py ping 8.8.8.8 --count 2 2>/dev/null | tail -1

echo ""
echo "=== Complete ==="
```

**Platform-Specific Features:**
- Uses native `ping` command (Linux format)
- Uses native `traceroute` command
- Compatible with bash scripting
- Works with cron for monitoring

### Step 4: Common Clio Commands

```bash
# Server health check
python3 netscan.py ports localhost --list 22,80,443,5432,6379

# Network discovery
python3 netscan.py scan 192.168.1 --timeout 0.3

# Check external connectivity
python3 netscan.py ping 8.8.8.8
python3 netscan.py dns google.com

# Diagnose connection issues
python3 netscan.py trace api.example.com
```

### Next Steps for Clio

1. Add to ABIOS startup checks
2. Create monitoring cron jobs
3. Report Linux-specific issues on GitHub

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of NetScan

### Step 1: Platform Detection

```python
import platform
from netscan import NetScan

ns = NetScan()

print(f"Platform: {platform.system()}")
print(f"Local IP: {ns.get_local_ip()}")
print(f"Hostname: {platform.node()}")
```

### Step 2: First Use - Cross-Platform Verification

```python
# Nexus: Same code works on Windows, Linux, macOS
from netscan import NetScan

def cross_platform_check():
    """Network check that works everywhere."""
    ns = NetScan()
    
    # Port scan (same API everywhere)
    results = ns.scan_ports("google.com", [80, 443])
    for port, is_open in results.items():
        print(f"  Port {port}: {'[OK]' if is_open else '[X]'}")
    
    # Ping (uses correct flags per platform)
    success, output = ns.ping("google.com", count=2)
    print(f"  Ping: {'[OK]' if success else '[X]'}")
    
    # DNS (universal)
    ip = ns.dns_lookup("google.com")
    print(f"  DNS: {ip}")

cross_platform_check()
```

### Step 3: Platform-Specific Considerations

**Windows:**
- Uses `tracert` instead of `traceroute`
- Ping uses `-n` flag instead of `-c`
- Paths use backslashes

**Linux:**
- Uses `traceroute` command
- Ping uses `-c` flag
- May need sudo for raw socket operations

**macOS:**
- Similar to Linux
- Uses BSD versions of commands

### Step 4: Common Nexus Commands

```bash
# Cross-platform command (same on all OSes)
python netscan.py ports google.com --list 80,443

# Platform-adaptive ping
python netscan.py ping google.com --count 3

# DNS (universal)
python netscan.py dns github.com
python netscan.py rdns 140.82.112.4
```

### Next Steps for Nexus

1. Test on all 3 platforms
2. Report platform-specific issues
3. Add to multi-platform workflows

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use NetScan without API costs

### Step 1: Verify Free Access

```bash
# NetScan requires NO API keys!
cd C:\Users\logan\OneDrive\Documents\AutoProjects\NetScan
python netscan.py --help
```

### Step 2: First Use - Batch Checks

```bash
# Bolt-friendly: Check multiple servers without API cost
python netscan.py port server1.example.com 80
python netscan.py port server2.example.com 80
python netscan.py port server3.example.com 80
```

### Step 3: Integration with Bolt Workflows

**Use Case: Batch Infrastructure Check**

```bash
#!/bin/bash
# bolt_batch_check.sh - No API cost!

SERVERS="web1.example.com web2.example.com db.example.com"

for server in $SERVERS; do
    echo "Checking $server..."
    python netscan.py ports $server --list 22,80,443 --timeout 1
done

echo "All checks complete (zero API cost)"
```

**Cost-Free Network Monitoring:**

```bash
# All operations use local networking, not AI APIs
python netscan.py scan 192.168.1 --timeout 0.3    # Free
python netscan.py ports example.com               # Free
python netscan.py ping google.com                 # Free
python netscan.py dns github.com                  # Free
```

### Step 4: Common Bolt Commands

```bash
# Bulk operations (save API calls!)
python netscan.py ports example.com --range 1-100

# Batch server check
for server in web1 web2 web3; do
    python netscan.py port $server.example.com 80
done

# Network discovery (no AI needed)
python netscan.py scan 10.0.0 --timeout 0.5
```

### Next Steps for Bolt

1. Add to Cline workflows
2. Use for repetitive connectivity tasks
3. Report any issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/NetScan/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message tool builder

---

## 🚀 QUICK COMMAND REFERENCE

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

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
