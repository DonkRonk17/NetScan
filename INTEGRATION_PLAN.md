# 🌐 NetScan - Integration Plan

**Version:** 1.0  
**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)

---

## 🎯 INTEGRATION GOALS

This document outlines how NetScan integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - future potential
4. Logan's workflows and automation

---

## 📦 BCH INTEGRATION

### Overview

NetScan provides network diagnostic capabilities that are essential for BCH operations, particularly for:
- Verifying server connectivity before operations
- Debugging connection issues between BCH components
- Monitoring service availability
- Network discovery for infrastructure mapping

### BCH Commands (Future)

When integrated with BCH, NetScan could provide commands like:

```
@netscan port backend.local 5000
@netscan ping 2s1c.local
@netscan dns api.beaconhq.local
```

### Implementation Steps (When Ready)

1. Add NetScan to BCH imports
2. Create command handlers for `@netscan` prefix
3. Map CLI commands to BCH command format
4. Add output formatting for BCH chat display
5. Test integration with all BCH clients (desktop, mobile)
6. Update BCH documentation

### Current Status

**Not currently integrated with BCH.** NetScan operates as a standalone CLI tool.

**Why:** BCH is still in Phase 0-1 development. Network diagnostics will be valuable once BCH has multiple services (frontend, backend, mobile) that need connectivity verification.

**Future Value:**
- Pre-flight checks before BCH operations
- Real-time connection debugging
- Infrastructure health monitoring
- Network topology discovery for BCH ecosystem

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Infrastructure verification before deployments | CLI + Python API | HIGH |
| **Atlas** | Debug network issues during tool builds | CLI + Python API | HIGH |
| **Clio** | Linux server diagnostics and monitoring | CLI (primary) | HIGH |
| **Nexus** | Cross-platform testing and validation | CLI + Python API | MEDIUM |
| **Bolt** | Batch connectivity checks | CLI (scripted) | MEDIUM |

### Agent-Specific Workflows

---

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Pre-deployment infrastructure verification and connectivity reviews.

**Integration Steps:**
1. Check infrastructure health before approving deployments
2. Verify BCH component connectivity
3. Debug connection issues reported by other agents
4. Monitor critical service availability

**Example Workflow:**

```python
# Forge session: Pre-deployment checklist
from netscan import NetScan

def verify_infrastructure():
    """Verify infrastructure before deployment approval."""
    ns = NetScan()
    
    checks = {
        "Backend API": ns.scan_port("api.beaconhq.local", 5000),
        "Database": ns.scan_port("db.beaconhq.local", 5432),
        "Redis Cache": ns.scan_port("cache.beaconhq.local", 6379),
        "Frontend": ns.scan_port("web.beaconhq.local", 3000),
    }
    
    failed = [name for name, status in checks.items() if not status]
    
    if failed:
        print(f"[X] Failed: {', '.join(failed)}")
        return False
    
    print("[OK] All infrastructure checks passed")
    return True

# Use in review workflow
if verify_infrastructure():
    print("Approved for deployment")
else:
    print("Deployment blocked - fix infrastructure issues first")
```

**Forge-Specific Commands:**

```bash
# Quick infrastructure health check
python netscan.py ports api.beaconhq.local --list 80,443,5000

# Verify database connectivity
python netscan.py port db.beaconhq.local 5432

# Check all BCH services
python netscan.py ports loadbalancer.beaconhq.local
```

---

#### Atlas (Executor / Builder)

**Primary Use Case:** Debug network issues during tool development and testing.

**Integration Steps:**
1. Verify API endpoints during integration work
2. Test network connectivity for new tools
3. Debug connection failures in test suites
4. Validate cross-platform network code

**Example Workflow:**

```python
# Atlas session: Testing API connectivity during tool build
from netscan import NetScan

def test_api_connectivity(api_host: str, api_port: int = 443) -> dict:
    """Test API connectivity before integration."""
    ns = NetScan()
    
    result = {
        "host": api_host,
        "port_open": ns.scan_port(api_host, api_port),
        "ip": ns.dns_lookup(api_host),
        "reachable": False,
    }
    
    # Additional ping check
    success, output = ns.ping(api_host, count=2)
    result["reachable"] = success
    
    return result

# Use during tool development
api_status = test_api_connectivity("api.github.com")
print(f"GitHub API status: {api_status}")
```

**Atlas-Specific Commands:**

```bash
# Test endpoint before API integration
python netscan.py port api.github.com 443

# Debug DNS issues
python netscan.py dns api.example.com
python netscan.py rdns 93.184.216.34

# Trace route to debug latency
python netscan.py trace api.example.com
```

---

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Linux server administration and network monitoring.

**Platform Considerations:**
- Native Linux networking commands used
- Works well with shell scripting
- Can be integrated into systemd services
- Compatible with cron jobs for monitoring

**Example Workflow:**

```bash
#!/bin/bash
# Clio: Server monitoring script

# Check critical services
python netscan.py port localhost 22   # SSH
python netscan.py port localhost 80   # Nginx
python netscan.py port localhost 5432 # PostgreSQL

# Scan local network for devices
python netscan.py scan 192.168.1 --timeout 0.3

# Check external connectivity
python netscan.py ping 8.8.8.8 --count 2
python netscan.py dns google.com
```

**Clio-Specific Commands:**

```bash
# Linux server health check
python netscan.py ports localhost --list 22,80,443,5432,6379

# Network interface IP
python netscan.py local

# Discover hosts on network segment
python netscan.py scan 10.0.0 --timeout 0.5
```

---

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform testing and connectivity validation.

**Cross-Platform Notes:**
- Uses platform-appropriate ping/traceroute commands
- Path handling works on all OSes
- Network API is consistent across platforms

**Example Workflow:**

```python
# Nexus: Cross-platform connectivity test
import platform
from netscan import NetScan

def cross_platform_test():
    """Test connectivity across platforms."""
    ns = NetScan()
    
    print(f"Platform: {platform.system()}")
    print(f"Local IP: {ns.get_local_ip()}")
    
    # Same API works everywhere
    results = ns.scan_ports("google.com", [80, 443])
    for port, is_open in results.items():
        status = "[OK]" if is_open else "[X]"
        print(f"  {status} Port {port}")
    
    # Ping uses correct flags per platform
    success, _ = ns.ping("google.com", count=2)
    print(f"Ping: {'[OK]' if success else '[X]'}")

cross_platform_test()
```

---

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Batch connectivity checks and automated monitoring.

**Cost Considerations:**
- NetScan requires zero API calls
- All operations are local/network-based
- Perfect for free execution without token cost

**Example Workflow:**

```bash
#!/bin/bash
# Bolt: Batch infrastructure check (no API cost!)

SERVERS="web1.example.com web2.example.com db.example.com"
PORTS="22,80,443"

for server in $SERVERS; do
    echo "Checking $server..."
    python netscan.py ports $server --list $PORTS --timeout 1
done

echo "All checks complete"
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With AgentHealth

**Correlation Use Case:** Monitor network health alongside agent health metrics.

**Integration Pattern:**

```python
from agenthealth import AgentHealth
from netscan import NetScan

health = AgentHealth()
ns = NetScan()

session_id = "network_check_001"

# Start health tracking
health.start_session("ATLAS", session_id=session_id)

try:
    # Perform network checks
    results = ns.scan_ports("api.example.com", [80, 443])
    
    if all(results.values()):
        health.heartbeat("ATLAS", status="active")
    else:
        health.log_error("ATLAS", "Network connectivity issues detected")
        
finally:
    health.end_session("ATLAS", session_id=session_id)
```

---

### With SynapseLink

**Notification Use Case:** Alert team when network issues are detected.

**Integration Pattern:**

```python
from synapselink import quick_send
from netscan import NetScan

ns = NetScan()

# Check critical service
is_open = ns.scan_port("db.example.com", 5432)

if not is_open:
    quick_send(
        "FORGE,LOGAN",
        "[ALERT] Database Port Closed",
        f"db.example.com:5432 is not responding.\n"
        f"Time: {datetime.now()}\n"
        f"Action: Investigate immediately.",
        priority="HIGH"
    )
else:
    quick_send(
        "TEAM",
        "[OK] Infrastructure Check Passed",
        "All critical services are responding normally.",
        priority="NORMAL"
    )
```

---

### With TaskQueuePro

**Task Management Use Case:** Queue network diagnostic tasks.

**Integration Pattern:**

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
    metadata={"tool": "NetScan", "check_type": "production"}
)

# Execute the check
queue.start_task(task_id)

try:
    results = ns.scan_ports("prod.example.com", [80, 443, 5432])
    
    queue.complete_task(task_id, result={
        "status": "success",
        "open_ports": [p for p, o in results.items() if o],
        "closed_ports": [p for p, o in results.items() if not o]
    })
except Exception as e:
    queue.fail_task(task_id, error=str(e))
```

---

### With MemoryBridge

**Context Persistence Use Case:** Store network check history.

**Integration Pattern:**

```python
from memorybridge import MemoryBridge
from netscan import NetScan
from datetime import datetime

memory = MemoryBridge()
ns = NetScan()

# Load history
network_history = memory.get("netscan_history", default=[])

# Perform check
check_result = {
    "timestamp": datetime.now().isoformat(),
    "host": "api.example.com",
    "ports_checked": [80, 443],
    "results": ns.scan_ports("api.example.com", [80, 443])
}

# Save to history
network_history.append(check_result)
memory.set("netscan_history", network_history)
memory.sync()
```

---

### With SessionReplay

**Debugging Use Case:** Record network operations for replay.

**Integration Pattern:**

```python
from sessionreplay import SessionReplay
from netscan import NetScan

replay = SessionReplay()
ns = NetScan()

session_id = replay.start_session("ATLAS", task="Network diagnostics")

try:
    replay.log_input(session_id, "Checking api.example.com ports 80,443")
    
    results = ns.scan_ports("api.example.com", [80, 443])
    
    replay.log_output(session_id, f"Results: {results}")
    replay.end_session(session_id, status="COMPLETED")
    
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
```

---

### With ContextCompressor

**Token Optimization Use Case:** Compress network scan reports.

**Integration Pattern:**

```python
from contextcompressor import ContextCompressor
from netscan import NetScan

compressor = ContextCompressor()
ns = NetScan()

# Generate detailed scan report
results = ns.scan_ports("example.com", list(range(1, 1000)))
report = f"Scanned 999 ports. Open: {[p for p,o in results.items() if o]}"

# Compress before sharing
compressed = compressor.compress_text(
    report,
    query="open ports summary",
    method="summary"
)

# Share compressed version (saves tokens)
print(compressed.compressed_text)
```

---

### With ConfigManager

**Configuration Use Case:** Centralize NetScan settings.

**Integration Pattern:**

```python
from configmanager import ConfigManager
from netscan import NetScan

config = ConfigManager()

# Load NetScan config
netscan_config = config.get("netscan", {
    "default_timeout": 2,
    "default_threads": 100,
    "common_hosts": ["api.example.com", "db.example.com"]
})

ns = NetScan()

# Use configured settings
for host in netscan_config["common_hosts"]:
    results = ns.scan_ports(
        host, 
        [80, 443], 
        timeout=netscan_config["default_timeout"],
        threads=netscan_config["default_threads"]
    )
    print(f"{host}: {results}")
```

---

### With ErrorRecovery

**Error Handling Use Case:** Auto-recovery from network failures.

**Integration Pattern:**

```python
from errorrecovery import ErrorRecovery
from netscan import NetScan

recovery = ErrorRecovery()
ns = NetScan()

@recovery.recoverable
def check_with_retry(host: str, port: int):
    """Check port with automatic retry on failure."""
    is_open = ns.scan_port(host, port)
    if not is_open:
        raise ConnectionError(f"{host}:{port} not responding")
    return is_open

# Will auto-retry on failure
try:
    result = check_with_retry("api.example.com", 443)
except ConnectionError as e:
    # Log error for future recovery suggestions
    recovery.log_error(str(e), category="network")
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features.

**Steps:**
1. ✅ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows.

**Steps:**
1. ☐ Add to agent startup routines (connectivity checks)
2. ☐ Create integration examples with existing tools
3. ☐ Update agent-specific workflows
4. ☐ Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted.

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements
3. ☐ Create advanced workflow examples
4. ☐ Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: Track
- Daily usage count: Track
- Integration with other tools: Track

**Efficiency Metrics:**
- Time saved on network debugging: Est. 10-30 min/session
- Reduced connectivity-related failures: Track
- Faster infrastructure verification: Track

**Quality Metrics:**
- Bug reports: Track
- Feature requests: Track
- User satisfaction: Qualitative

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from netscan import NetScan, COMMON_PORTS

# Import with config
from netscan import NetScan, DEFAULT_TIMEOUT, MAX_THREADS
```

### Configuration Integration

**Config File:** Not currently used (all options via CLI/API)

**Future Config Path:** `~/.netscanrc`

**Example Future Config:**
```json
{
  "default_timeout": 2,
  "default_threads": 100,
  "favorite_hosts": ["api.example.com", "db.example.com"]
}
```

### Error Handling Integration

**Standardized Exit Codes:**
- 0: Success
- 1: General error
- 2: Network error (host unreachable)
- 3: Timeout

### Logging Integration

**Log Format:** Stdout/stderr (no file logging currently)

**Future Enhancement:** Add `--log-file` option for persistent logging

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed for bug fixes
- Major updates (v2.0+): For significant feature additions
- Security patches: Immediate

### Support Channels

- GitHub Issues: Bug reports and feature requests
- Synapse: Team Brain discussions
- Direct to Builder: Complex issues

### Known Limitations

1. Network scanning requires appropriate permissions
2. Some operations need elevated privileges (raw sockets)
3. Traceroute command varies by platform
4. Large scans can be slow (network I/O bound)

**Planned Improvements:**
- v1.1: Add JSON output format
- v1.2: Add configuration file support
- v1.3: Add scheduling/monitoring mode
- v2.0: Add web interface option

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/NetScan

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
