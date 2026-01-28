# 🌐 NetScan - Integration Examples

**10 Copy-Paste-Ready Integration Patterns**

## 🎯 INTEGRATION PHILOSOPHY

NetScan is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: NetScan + AgentHealth](#pattern-1-netscan--agenthealth)
2. [Pattern 2: NetScan + SynapseLink](#pattern-2-netscan--synapselink)
3. [Pattern 3: NetScan + TaskQueuePro](#pattern-3-netscan--taskqueuepro)
4. [Pattern 4: NetScan + MemoryBridge](#pattern-4-netscan--memorybridge)
5. [Pattern 5: NetScan + SessionReplay](#pattern-5-netscan--sessionreplay)
6. [Pattern 6: NetScan + ContextCompressor](#pattern-6-netscan--contextcompressor)
7. [Pattern 7: NetScan + ConfigManager](#pattern-7-netscan--configmanager)
8. [Pattern 8: NetScan + ErrorRecovery](#pattern-8-netscan--errorrecovery)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: NetScan + AgentHealth

**Use Case:** Correlate network connectivity with agent health metrics.

**Why:** Understand how network issues affect agent performance.

**Code:**

```python
from agenthealth import AgentHealth
from netscan import NetScan
from datetime import datetime

# Initialize both tools
health = AgentHealth()
ns = NetScan()

# Start session with shared ID
session_id = f"network_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

health.start_session("ATLAS", session_id=session_id)

try:
    # Perform network checks
    health.heartbeat("ATLAS", status="checking_network")
    
    results = ns.scan_ports("api.example.com", [80, 443, 5000])
    
    # Count open ports
    open_ports = [p for p, is_open in results.items() if is_open]
    closed_ports = [p for p, is_open in results.items() if not is_open]
    
    if closed_ports:
        health.log_error("ATLAS", f"Closed ports: {closed_ports}")
    else:
        health.heartbeat("ATLAS", status="network_ok")
    
    print(f"Open ports: {open_ports}")
    print(f"Closed ports: {closed_ports}")
    
except Exception as e:
    health.log_error("ATLAS", f"Network check failed: {e}")
    raise
    
finally:
    health.end_session("ATLAS", session_id=session_id)
```

**Result:** Correlated health and network data for analysis.

---

## Pattern 2: NetScan + SynapseLink

**Use Case:** Alert Team Brain when network issues are detected.

**Why:** Keep team informed of infrastructure problems automatically.

**Code:**

```python
from synapselink import quick_send
from netscan import NetScan
from datetime import datetime

ns = NetScan()

# Define critical services to monitor
critical_services = [
    ("Database", "db.example.com", 5432),
    ("API Server", "api.example.com", 5000),
    ("Redis Cache", "cache.example.com", 6379),
]

# Check each service
failures = []
successes = []

for name, host, port in critical_services:
    is_open = ns.scan_port(host, port, timeout=3)
    if is_open:
        successes.append(f"[OK] {name} ({host}:{port})")
    else:
        failures.append(f"[X] {name} ({host}:{port})")

# Send notification based on results
if failures:
    quick_send(
        "FORGE,LOGAN",
        "[ALERT] Network Issues Detected",
        f"Time: {datetime.now()}\n\n"
        f"Failed Services:\n" + "\n".join(failures) + "\n\n"
        f"Working Services:\n" + "\n".join(successes) + "\n\n"
        f"Action: Investigate immediately.",
        priority="HIGH"
    )
else:
    quick_send(
        "TEAM",
        "[OK] Infrastructure Health Check Passed",
        f"Time: {datetime.now()}\n\n"
        f"All {len(critical_services)} services responding normally:\n" +
        "\n".join(successes),
        priority="NORMAL"
    )
```

**Result:** Team stays informed without manual status updates.

---

## Pattern 3: NetScan + TaskQueuePro

**Use Case:** Queue and track network diagnostic tasks.

**Why:** Centralized task management for network operations.

**Code:**

```python
from taskqueuepro import TaskQueuePro
from netscan import NetScan

queue = TaskQueuePro()
ns = NetScan()

# Create network check task
task_id = queue.create_task(
    title="Check production infrastructure",
    agent="ATLAS",
    priority=2,
    metadata={
        "tool": "NetScan",
        "check_type": "production",
        "hosts": ["web.example.com", "api.example.com", "db.example.com"]
    }
)

# Mark as in-progress
queue.start_task(task_id)

try:
    hosts_to_check = [
        ("web.example.com", [80, 443]),
        ("api.example.com", [5000]),
        ("db.example.com", [5432]),
    ]
    
    all_results = {}
    
    for host, ports in hosts_to_check:
        results = ns.scan_ports(host, ports)
        all_results[host] = results
    
    # Complete task with results
    queue.complete_task(task_id, result={
        "status": "success",
        "results": all_results,
        "summary": f"Checked {len(hosts_to_check)} hosts"
    })
    
except Exception as e:
    queue.fail_task(task_id, error=str(e))
```

**Result:** Centralized task tracking across all network operations.

---

## Pattern 4: NetScan + MemoryBridge

**Use Case:** Store network check history for trend analysis.

**Why:** Track connectivity over time, identify patterns.

**Code:**

```python
from memorybridge import MemoryBridge
from netscan import NetScan
from datetime import datetime

memory = MemoryBridge()
ns = NetScan()

# Load existing history
network_history = memory.get("netscan_history", default=[])

# Perform check
hosts = ["api.example.com", "db.example.com"]
check_result = {
    "timestamp": datetime.now().isoformat(),
    "hosts": {},
    "all_ok": True
}

for host in hosts:
    results = ns.scan_ports(host, [80, 443])
    check_result["hosts"][host] = results
    if not all(results.values()):
        check_result["all_ok"] = False

# Append to history
network_history.append(check_result)

# Keep last 100 entries
network_history = network_history[-100:]

# Save back to memory
memory.set("netscan_history", network_history)
memory.sync()

# Report
if check_result["all_ok"]:
    print(f"[OK] All {len(hosts)} hosts healthy")
else:
    print(f"[!] Issues detected in network check")
    
print(f"History now has {len(network_history)} entries")
```

**Result:** Historical data persisted for trend analysis.

---

## Pattern 5: NetScan + SessionReplay

**Use Case:** Record network diagnostic sessions for debugging.

**Why:** Replay network operations when investigating issues.

**Code:**

```python
from sessionreplay import SessionReplay
from netscan import NetScan

replay = SessionReplay()
ns = NetScan()

# Start recording session
session_id = replay.start_session("ATLAS", task="Network diagnostics for API issue")

try:
    # Log what we're checking
    replay.log_input(session_id, "Checking api.example.com connectivity")
    
    # DNS check
    ip = ns.dns_lookup("api.example.com")
    replay.log_output(session_id, f"DNS resolved: {ip}")
    
    # Ping check
    success, ping_output = ns.ping("api.example.com", count=2)
    replay.log_output(session_id, f"Ping: {'Success' if success else 'Failed'}")
    
    # Port check
    results = ns.scan_ports("api.example.com", [80, 443])
    replay.log_output(session_id, f"Port scan: {results}")
    
    # Determine outcome
    if ip and success and all(results.values()):
        replay.log_output(session_id, "CONCLUSION: API is fully reachable")
        replay.end_session(session_id, status="COMPLETED")
    else:
        replay.log_output(session_id, "CONCLUSION: Connectivity issues detected")
        replay.end_session(session_id, status="COMPLETED_WITH_ISSUES")
    
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    raise
```

**Result:** Full session replay available for debugging.

---

## Pattern 6: NetScan + ContextCompressor

**Use Case:** Compress large network scan reports before sharing.

**Why:** Save tokens when sharing extensive scan results.

**Code:**

```python
from contextcompressor import ContextCompressor
from netscan import NetScan

compressor = ContextCompressor()
ns = NetScan()

# Perform extensive scan
host = "example.com"
ports = list(range(1, 1000))  # Scan 999 ports

results = ns.scan_ports(host, ports, timeout=0.5)

# Generate detailed report
open_ports = [p for p, is_open in results.items() if is_open]
closed_ports = [p for p, is_open in results.items() if not is_open]

full_report = f"""
Network Scan Report
==================
Host: {host}
Ports Scanned: {len(ports)}
Open Ports: {len(open_ports)}
Closed Ports: {len(closed_ports)}

Open Port Details:
{chr(10).join(f'  - Port {p}' for p in sorted(open_ports))}

Scan Summary:
- Total ports scanned: {len(ports)}
- Success rate: {len(open_ports)}/{len(ports)} open
"""

# Compress before sharing
compressed = compressor.compress_text(
    full_report,
    query="open ports summary",
    method="summary"
)

print(f"Original: ~{len(full_report)} chars")
print(f"Compressed: ~{len(compressed.compressed_text)} chars")
print(f"Savings: {compressed.estimated_token_savings} tokens")
print()
print("Compressed Summary:")
print(compressed.compressed_text)
```

**Result:** 70-90% token savings on large reports.

---

## Pattern 7: NetScan + ConfigManager

**Use Case:** Centralize network monitoring configuration.

**Why:** Share settings across tools and agents.

**Code:**

```python
from configmanager import ConfigManager
from netscan import NetScan

config = ConfigManager()

# Load or create default NetScan config
netscan_config = config.get("netscan", {
    "default_timeout": 2,
    "default_threads": 100,
    "monitored_hosts": [
        {"name": "API", "host": "api.example.com", "ports": [80, 443]},
        {"name": "Database", "host": "db.example.com", "ports": [5432]},
        {"name": "Cache", "host": "cache.example.com", "ports": [6379]},
    ],
    "alert_on_failure": True
})

# Use config for monitoring
ns = NetScan()

for service in netscan_config["monitored_hosts"]:
    results = ns.scan_ports(
        service["host"], 
        service["ports"],
        timeout=netscan_config["default_timeout"],
        threads=netscan_config["default_threads"]
    )
    
    status = "[OK]" if all(results.values()) else "[X]"
    print(f"{status} {service['name']}: {service['host']}")

# Update config if needed
if netscan_config["default_timeout"] < 3:
    config.set("netscan.default_timeout", 3)
    config.save()
    print("Updated timeout to 3 seconds")
```

**Result:** Centralized, shareable configuration.

---

## Pattern 8: NetScan + ErrorRecovery

**Use Case:** Auto-retry network operations on failure.

**Why:** Handle transient network issues gracefully.

**Code:**

```python
from errorrecovery import ErrorRecovery
from netscan import NetScan
import time

recovery = ErrorRecovery()
ns = NetScan()

def check_service_with_retry(host: str, port: int, max_retries: int = 3) -> bool:
    """Check service with automatic retry on failure."""
    
    for attempt in range(max_retries):
        is_open = ns.scan_port(host, port, timeout=2)
        
        if is_open:
            return True
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"  Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
    
    # Log persistent failure
    recovery.log_error(
        f"Service {host}:{port} failed after {max_retries} attempts",
        category="network",
        severity="high"
    )
    
    return False

# Use the retry function
services = [
    ("api.example.com", 443),
    ("db.example.com", 5432),
]

for host, port in services:
    print(f"Checking {host}:{port}...")
    result = check_service_with_retry(host, port)
    status = "[OK]" if result else "[X] FAILED"
    print(f"  {status}")
```

**Result:** Resilient network checks with automatic retry.

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete network diagnostic workflow using multiple tools.

**Why:** Demonstrate real production scenario.

**Code:**

```python
from taskqueuepro import TaskQueuePro
from sessionreplay import SessionReplay
from agenthealth import AgentHealth
from synapselink import quick_send
from netscan import NetScan
from datetime import datetime

# Initialize all tools
queue = TaskQueuePro()
replay = SessionReplay()
health = AgentHealth()
ns = NetScan()

# Create orchestrated workflow
task_id = queue.create_task("Full network diagnostic", agent="ATLAS", priority=1)
session_id = replay.start_session("ATLAS", task="Network diagnostic workflow")
health.start_session("ATLAS", session_id=session_id)

try:
    # Start work
    queue.start_task(task_id)
    health.heartbeat("ATLAS", status="running_diagnostics")
    replay.log_input(session_id, "Starting comprehensive network check")
    
    # Define what to check
    checks = [
        ("DNS Resolution", lambda: ns.dns_lookup("api.example.com") is not None),
        ("Ping", lambda: ns.ping("api.example.com", count=2)[0]),
        ("Port 443", lambda: ns.scan_port("api.example.com", 443)),
        ("Port 80", lambda: ns.scan_port("api.example.com", 80)),
    ]
    
    results = {}
    all_passed = True
    
    for name, check_func in checks:
        replay.log_input(session_id, f"Running: {name}")
        passed = check_func()
        results[name] = passed
        replay.log_output(session_id, f"{name}: {'PASS' if passed else 'FAIL'}")
        
        if not passed:
            all_passed = False
            health.log_error("ATLAS", f"Check failed: {name}")
    
    # Complete successfully
    queue.complete_task(task_id, result=results)
    replay.end_session(session_id, status="COMPLETED")
    health.end_session("ATLAS", session_id=session_id, status="success")
    
    # Notify team
    if all_passed:
        quick_send("TEAM", "Network Check Passed", 
                   f"All {len(checks)} checks passed at {datetime.now()}")
    else:
        quick_send("FORGE,LOGAN", "Network Issues Found",
                   f"Failed checks: {[k for k,v in results.items() if not v]}",
                   priority="HIGH")
    
except Exception as e:
    # Handle failure
    queue.fail_task(task_id, error=str(e))
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    
    quick_send("FORGE,LOGAN", "Network Check Failed", str(e), priority="HIGH")
    raise
```

**Result:** Fully instrumented, coordinated workflow.

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - infrastructure monitoring dashboard.

**Why:** Production-grade agent operation.

**Code:**

```python
#!/usr/bin/env python3
"""
Team Brain Infrastructure Monitor
Uses NetScan with full tool integration
"""

from netscan import NetScan
from synapselink import quick_send
from memorybridge import MemoryBridge
from configmanager import ConfigManager
from agenthealth import AgentHealth
from datetime import datetime
import json

class InfrastructureMonitor:
    """Full Team Brain infrastructure monitoring."""
    
    def __init__(self):
        self.ns = NetScan()
        self.memory = MemoryBridge()
        self.config = ConfigManager()
        self.health = AgentHealth()
        
        # Load config
        self.settings = self.config.get("infra_monitor", {
            "check_interval": 300,  # 5 minutes
            "alert_threshold": 2,   # Failures before alert
            "hosts": [
                {"name": "API", "host": "api.example.com", "ports": [80, 443]},
                {"name": "Database", "host": "db.example.com", "ports": [5432]},
            ]
        })
    
    def run_check(self) -> dict:
        """Run infrastructure check."""
        session_id = f"infra_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.health.start_session("MONITOR", session_id=session_id)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "all_ok": True
        }
        
        try:
            for service in self.settings["hosts"]:
                port_results = self.ns.scan_ports(
                    service["host"], 
                    service["ports"]
                )
                
                is_ok = all(port_results.values())
                results["checks"][service["name"]] = {
                    "host": service["host"],
                    "ports": port_results,
                    "ok": is_ok
                }
                
                if not is_ok:
                    results["all_ok"] = False
            
            self.health.heartbeat("MONITOR", status="check_complete")
            
        finally:
            self.health.end_session("MONITOR", session_id=session_id)
        
        return results
    
    def store_results(self, results: dict):
        """Store results in memory."""
        history = self.memory.get("infra_history", default=[])
        history.append(results)
        history = history[-100:]  # Keep last 100
        self.memory.set("infra_history", history)
        self.memory.sync()
    
    def check_for_alerts(self, results: dict):
        """Send alerts if needed."""
        if not results["all_ok"]:
            failures = [
                name for name, data in results["checks"].items() 
                if not data["ok"]
            ]
            
            quick_send(
                "FORGE,LOGAN",
                "[ALERT] Infrastructure Issues",
                f"Failed services: {', '.join(failures)}\n"
                f"Time: {results['timestamp']}\n"
                f"Action required.",
                priority="HIGH"
            )
    
    def run(self):
        """Run single check cycle."""
        print(f"Infrastructure check starting at {datetime.now()}")
        
        results = self.run_check()
        self.store_results(results)
        self.check_for_alerts(results)
        
        # Print summary
        for name, data in results["checks"].items():
            status = "[OK]" if data["ok"] else "[X]"
            print(f"  {status} {name}")
        
        return results["all_ok"]

# Usage
if __name__ == "__main__":
    monitor = InfrastructureMonitor()
    all_ok = monitor.run()
    
    if all_ok:
        print("\n[OK] All infrastructure healthy")
    else:
        print("\n[!] Issues detected - check alerts")
```

**Result:** Production-grade monitoring with full Team Brain integration.

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ AgentHealth - Health correlation
2. ✅ SynapseLink - Team notifications
3. ✅ ErrorRecovery - Retry handling

**Week 2 (Productivity):**
4. ☐ TaskQueuePro - Task management
5. ☐ MemoryBridge - Data persistence
6. ☐ ConfigManager - Configuration

**Week 3 (Advanced):**
7. ☐ SessionReplay - Debugging
8. ☐ ContextCompressor - Token optimization
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**

```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from netscan import NetScan
from synapselink import quick_send
```

**Version Conflicts:**

```bash
# Check versions
python netscan.py --help

# Update if needed
cd AutoProjects/NetScan
git pull origin main
```

**Network Permission Issues:**

```python
# Some operations may need elevated privileges
# Try running as administrator/root for:
# - Raw socket operations
# - Network interface listing
# - Some traceroute modes
```

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
