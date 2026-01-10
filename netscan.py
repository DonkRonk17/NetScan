#!/usr/bin/env python3
"""
NetScan - CLI Network Utilities Toolkit
A unified interface for common network operations - port scanning, ping, DNS lookup, and more.
"""

import os
import sys
import io
import socket
import subprocess
import argparse
import time
import platform
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Config ---
DEFAULT_TIMEOUT = 2
MAX_THREADS = 100
COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
    27017: "MongoDB"
}

class NetScan:
    """Network utilities toolkit"""
    
    @staticmethod
    def scan_port(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> bool:
        """Check if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except socket.gaierror:
            return False
        except socket.error:
            return False
        except Exception:
            return False
    
    @staticmethod
    def scan_ports(host: str, ports: List[int], timeout: float = DEFAULT_TIMEOUT, threads: int = MAX_THREADS) -> Dict[int, bool]:
        """Scan multiple ports concurrently"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_port = {executor.submit(NetScan.scan_port, host, port, timeout): port for port in ports}
            
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    results[port] = future.result()
                except Exception:
                    results[port] = False
        
        return results
    
    @staticmethod
    def ping(host: str, count: int = 4) -> Tuple[bool, str]:
        """Ping a host"""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        
        try:
            command = ['ping', param, str(count), host]
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=count * 2 + 5,
                text=True
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            return success, output
        except subprocess.TimeoutExpired:
            return False, "Timeout: Host did not respond"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def dns_lookup(host: str) -> Optional[str]:
        """Resolve hostname to IP"""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return None
        except Exception:
            return None
    
    @staticmethod
    def reverse_dns(ip: str) -> Optional[str]:
        """Resolve IP to hostname"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None
        except Exception:
            return None
    
    @staticmethod
    def get_local_ip() -> str:
        """Get local IP address"""
        try:
            # Create socket to external address (doesn't actually connect)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def scan_network(network_prefix: str, timeout: float = 0.5) -> List[str]:
        """Scan network for active hosts"""
        active_hosts = []
        
        # Generate IP range
        ips = [f"{network_prefix}.{i}" for i in range(1, 255)]
        
        def check_host(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                # Try common ports
                for port in [80, 443, 22, 445]:
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        sock.close()
                        return ip
                sock.close()
            except:
                pass
            return None
        
        print(f"🔍 Scanning {network_prefix}.1-254...")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(check_host, ip): ip for ip in ips}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    active_hosts.append(result)
                    print(f"  ✅ Found: {result}")
        
        return sorted(active_hosts, key=lambda x: int(x.split('.')[-1]))
    
    @staticmethod
    def traceroute(host: str, max_hops: int = 30) -> str:
        """Trace route to host"""
        param = '-h' if platform.system().lower() == 'windows' else '-m'
        command_name = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
        
        try:
            command = [command_name, param, str(max_hops), host]
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=max_hops * 3,
                text=True
            )
            
            return result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            return "Timeout: Traceroute took too long"
        except FileNotFoundError:
            return f"Error: {command_name} command not found"
        except Exception as e:
            return f"Error: {str(e)}"


def format_port_results(host: str, results: Dict[int, bool]):
    """Pretty print port scan results"""
    open_ports = {port: is_open for port, is_open in results.items() if is_open}
    
    if not open_ports:
        print(f"\n❌ No open ports found on {host}\n")
        return
    
    print(f"\n✅ Open ports on {host}:\n")
    print("Port      Service")
    print("-" * 40)
    
    for port in sorted(open_ports.keys()):
        service = COMMON_PORTS.get(port, "Unknown")
        print(f"{port:<10}{service}")
    
    print(f"\n📊 Total: {len(open_ports)} open port(s) found\n")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="NetScan - CLI Network Utilities Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  netscan port example.com 80                    # Check single port
  netscan ports example.com                      # Scan common ports
  netscan ports example.com --range 1-1000       # Scan port range
  netscan ping google.com                        # Ping host
  netscan dns example.com                        # DNS lookup
  netscan rdns 8.8.8.8                          # Reverse DNS
  netscan local                                  # Show local IP
  netscan scan 192.168.1                        # Scan local network
  netscan trace google.com                       # Traceroute
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Port command
    port_parser = subparsers.add_parser('port', help='Check if a single port is open')
    port_parser.add_argument('host', help='Target host (IP or domain)')
    port_parser.add_argument('port', type=int, help='Port number')
    port_parser.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT, help='Timeout in seconds')
    
    # Ports command
    ports_parser = subparsers.add_parser('ports', help='Scan multiple ports')
    ports_parser.add_argument('host', help='Target host (IP or domain)')
    ports_parser.add_argument('--range', help='Port range (e.g., 1-1000)')
    ports_parser.add_argument('--list', help='Comma-separated port list (e.g., 80,443,3306)')
    ports_parser.add_argument('--common', action='store_true', help='Scan common ports only (default)')
    ports_parser.add_argument('--timeout', type=float, default=DEFAULT_TIMEOUT, help='Timeout in seconds')
    ports_parser.add_argument('--threads', type=int, default=MAX_THREADS, help='Number of threads')
    
    # Ping command
    ping_parser = subparsers.add_parser('ping', help='Ping a host')
    ping_parser.add_argument('host', help='Target host (IP or domain)')
    ping_parser.add_argument('--count', type=int, default=4, help='Number of pings')
    
    # DNS command
    dns_parser = subparsers.add_parser('dns', help='DNS lookup (hostname to IP)')
    dns_parser.add_argument('host', help='Hostname to resolve')
    
    # Reverse DNS command
    rdns_parser = subparsers.add_parser('rdns', help='Reverse DNS lookup (IP to hostname)')
    rdns_parser.add_argument('ip', help='IP address to resolve')
    
    # Local IP command
    local_parser = subparsers.add_parser('local', help='Show local IP address')
    
    # Network scan command
    scan_parser = subparsers.add_parser('scan', help='Scan local network for active hosts')
    scan_parser.add_argument('network', help='Network prefix (e.g., 192.168.1)')
    scan_parser.add_argument('--timeout', type=float, default=0.5, help='Timeout per host')
    
    # Traceroute command
    trace_parser = subparsers.add_parser('trace', help='Traceroute to host')
    trace_parser.add_argument('host', help='Target host (IP or domain)')
    trace_parser.add_argument('--hops', type=int, default=30, help='Maximum hops')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    ns = NetScan()
    
    # Execute command
    if args.command == 'port':
        print(f"\n🔍 Checking {args.host}:{args.port}...")
        is_open = ns.scan_port(args.host, args.port, args.timeout)
        
        if is_open:
            service = COMMON_PORTS.get(args.port, "Unknown")
            print(f"✅ Port {args.port} is OPEN ({service})\n")
        else:
            print(f"❌ Port {args.port} is CLOSED or FILTERED\n")
    
    elif args.command == 'ports':
        # Determine which ports to scan
        if args.list:
            ports = [int(p.strip()) for p in args.list.split(',')]
        elif args.range:
            start, end = map(int, args.range.split('-'))
            ports = list(range(start, end + 1))
        else:
            # Scan common ports by default
            ports = list(COMMON_PORTS.keys())
        
        print(f"\n🔍 Scanning {len(ports)} port(s) on {args.host}...")
        print(f"⏱️  Timeout: {args.timeout}s | Threads: {args.threads}\n")
        
        start_time = time.time()
        results = ns.scan_ports(args.host, ports, args.timeout, args.threads)
        elapsed = time.time() - start_time
        
        format_port_results(args.host, results)
        print(f"⏱️  Scan completed in {elapsed:.2f} seconds\n")
    
    elif args.command == 'ping':
        print(f"\n🏓 Pinging {args.host}...\n")
        success, output = ns.ping(args.host, args.count)
        
        print(output)
        
        if success:
            print(f"\n✅ {args.host} is reachable\n")
        else:
            print(f"\n❌ {args.host} is unreachable\n")
    
    elif args.command == 'dns':
        print(f"\n🔍 Resolving {args.host}...")
        ip = ns.dns_lookup(args.host)
        
        if ip:
            print(f"✅ {args.host} → {ip}\n")
        else:
            print(f"❌ Could not resolve {args.host}\n")
    
    elif args.command == 'rdns':
        print(f"\n🔍 Reverse resolving {args.ip}...")
        hostname = ns.reverse_dns(args.ip)
        
        if hostname:
            print(f"✅ {args.ip} → {hostname}\n")
        else:
            print(f"❌ Could not reverse resolve {args.ip}\n")
    
    elif args.command == 'local':
        local_ip = ns.get_local_ip()
        hostname = socket.gethostname()
        
        print(f"\n💻 Local Network Information:\n")
        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}\n")
    
    elif args.command == 'scan':
        print(f"\n🌐 Scanning network {args.network}.0/24...\n")
        start_time = time.time()
        
        hosts = ns.scan_network(args.network, args.timeout)
        elapsed = time.time() - start_time
        
        if hosts:
            print(f"\n✅ Found {len(hosts)} active host(s):\n")
            for host in hosts:
                # Try to get hostname
                hostname = ns.reverse_dns(host)
                if hostname:
                    print(f"  {host} ({hostname})")
                else:
                    print(f"  {host}")
            print(f"\n⏱️  Scan completed in {elapsed:.2f} seconds\n")
        else:
            print(f"\n❌ No active hosts found\n")
    
    elif args.command == 'trace':
        print(f"\n🗺️  Tracing route to {args.host}...\n")
        output = ns.traceroute(args.host, args.hops)
        print(output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 NetScan interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
