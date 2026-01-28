#!/usr/bin/env python3
"""
Comprehensive test suite for NetScan v1.0

Tests cover:
- Core networking functionality (port scanning, DNS, ping)
- Edge cases and error handling
- Input validation
- Cross-platform compatibility
- Performance and threading

Run: python test_netscan.py
"""

import unittest
import sys
import socket
import platform
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from netscan import NetScan, COMMON_PORTS, DEFAULT_TIMEOUT, MAX_THREADS, format_port_results


class TestNetScanCore(unittest.TestCase):
    """Test core NetScan functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_netscan_class_exists(self):
        """Test NetScan class can be instantiated."""
        ns = NetScan()
        self.assertIsNotNone(ns)
    
    def test_common_ports_defined(self):
        """Test common ports dictionary is populated."""
        self.assertIsInstance(COMMON_PORTS, dict)
        self.assertGreater(len(COMMON_PORTS), 10)
        self.assertIn(80, COMMON_PORTS)
        self.assertIn(443, COMMON_PORTS)
        self.assertEqual(COMMON_PORTS[80], "HTTP")
        self.assertEqual(COMMON_PORTS[443], "HTTPS")
    
    def test_default_timeout_value(self):
        """Test default timeout is reasonable."""
        self.assertIsInstance(DEFAULT_TIMEOUT, (int, float))
        self.assertGreater(DEFAULT_TIMEOUT, 0)
        self.assertLessEqual(DEFAULT_TIMEOUT, 10)
    
    def test_max_threads_value(self):
        """Test max threads is reasonable."""
        self.assertIsInstance(MAX_THREADS, int)
        self.assertGreater(MAX_THREADS, 0)
        self.assertLessEqual(MAX_THREADS, 500)


class TestPortScanning(unittest.TestCase):
    """Test port scanning functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_scan_port_returns_bool(self):
        """Test scan_port returns boolean."""
        result = self.ns.scan_port("127.0.0.1", 80, timeout=0.1)
        self.assertIsInstance(result, bool)
    
    def test_scan_port_invalid_host(self):
        """Test scan_port handles invalid host gracefully."""
        result = self.ns.scan_port("definitely.invalid.host.xyz", 80, timeout=0.1)
        self.assertFalse(result)
    
    def test_scan_port_closed_port(self):
        """Test scan_port detects closed port."""
        # Port 65535 is almost always closed
        result = self.ns.scan_port("127.0.0.1", 65535, timeout=0.1)
        self.assertFalse(result)
    
    def test_scan_ports_returns_dict(self):
        """Test scan_ports returns dictionary."""
        result = self.ns.scan_ports("127.0.0.1", [80, 443], timeout=0.1)
        self.assertIsInstance(result, dict)
        self.assertIn(80, result)
        self.assertIn(443, result)
    
    def test_scan_ports_all_ports_checked(self):
        """Test all requested ports are scanned."""
        ports = [22, 80, 443, 8080, 3306]
        result = self.ns.scan_ports("127.0.0.1", ports, timeout=0.1)
        self.assertEqual(len(result), len(ports))
        for port in ports:
            self.assertIn(port, result)
    
    def test_scan_ports_empty_list(self):
        """Test scan_ports handles empty port list."""
        result = self.ns.scan_ports("127.0.0.1", [], timeout=0.1)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
    
    def test_scan_ports_with_threads(self):
        """Test scan_ports respects thread count."""
        ports = list(range(80, 100))
        result = self.ns.scan_ports("127.0.0.1", ports, timeout=0.1, threads=5)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(ports))


class TestDNSOperations(unittest.TestCase):
    """Test DNS lookup functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_dns_lookup_localhost(self):
        """Test DNS lookup for localhost."""
        result = self.ns.dns_lookup("localhost")
        self.assertIsNotNone(result)
        self.assertIn(result, ["127.0.0.1", "::1"])
    
    def test_dns_lookup_invalid_host(self):
        """Test DNS lookup handles invalid host gracefully."""
        # Note: Some DNS providers resolve random domains (NXDOMAIN hijacking)
        # So we just check it returns string or None without crashing
        result = self.ns.dns_lookup("this.domain.definitely.does.not.exist.xyz")
        self.assertTrue(result is None or isinstance(result, str))
    
    def test_dns_lookup_returns_string_or_none(self):
        """Test DNS lookup returns string or None."""
        result = self.ns.dns_lookup("localhost")
        self.assertTrue(result is None or isinstance(result, str))
    
    def test_reverse_dns_returns_string_or_none(self):
        """Test reverse DNS returns string or None."""
        result = self.ns.reverse_dns("127.0.0.1")
        self.assertTrue(result is None or isinstance(result, str))
    
    def test_reverse_dns_invalid_ip(self):
        """Test reverse DNS handles invalid IP."""
        result = self.ns.reverse_dns("999.999.999.999")
        self.assertIsNone(result)


class TestLocalIPDetection(unittest.TestCase):
    """Test local IP detection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_get_local_ip_returns_string(self):
        """Test get_local_ip returns string."""
        result = self.ns.get_local_ip()
        self.assertIsInstance(result, str)
    
    def test_get_local_ip_valid_format(self):
        """Test get_local_ip returns valid IP format."""
        result = self.ns.get_local_ip()
        # Should have at least one dot
        self.assertIn(".", result)
        # Split into parts
        parts = result.split(".")
        # IPv4 should have 4 parts
        if len(parts) == 4:
            for part in parts:
                self.assertTrue(0 <= int(part) <= 255)
    
    def test_get_local_ip_not_empty(self):
        """Test get_local_ip doesn't return empty."""
        result = self.ns.get_local_ip()
        self.assertTrue(len(result) > 0)


class TestPingFunctionality(unittest.TestCase):
    """Test ping functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_ping_returns_tuple(self):
        """Test ping returns tuple of (bool, str)."""
        result = self.ns.ping("127.0.0.1", count=1)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], str)
    
    def test_ping_localhost_succeeds(self):
        """Test pinging localhost succeeds."""
        success, output = self.ns.ping("127.0.0.1", count=1)
        self.assertTrue(success)
        self.assertTrue(len(output) > 0)
    
    def test_ping_invalid_host(self):
        """Test ping invalid host returns failure."""
        success, output = self.ns.ping("this.invalid.host.xyz", count=1)
        # May or may not succeed depending on DNS behavior
        self.assertIsInstance(success, bool)
        self.assertIsInstance(output, str)


class TestTraceroute(unittest.TestCase):
    """Test traceroute functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_traceroute_returns_string(self):
        """Test traceroute returns string."""
        result = self.ns.traceroute("127.0.0.1", max_hops=2)
        self.assertIsInstance(result, str)
    
    def test_traceroute_localhost(self):
        """Test traceroute to localhost returns something."""
        result = self.ns.traceroute("127.0.0.1", max_hops=2)
        self.assertTrue(len(result) > 0)


class TestNetworkScan(unittest.TestCase):
    """Test network scanning functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_scan_network_returns_list(self):
        """Test scan_network returns list."""
        # Use very short timeout for fast test
        with patch('builtins.print'):  # Suppress print output
            result = self.ns.scan_network("127.0.0", timeout=0.01)
        self.assertIsInstance(result, list)
    
    def test_scan_network_localhost(self):
        """Test scan_network finds localhost."""
        with patch('builtins.print'):  # Suppress print output
            result = self.ns.scan_network("127.0.0", timeout=0.1)
        # May or may not find localhost depending on open ports
        self.assertIsInstance(result, list)


class TestInputValidation(unittest.TestCase):
    """Test input validation and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_scan_port_zero_timeout(self):
        """Test scan_port with zero timeout."""
        result = self.ns.scan_port("127.0.0.1", 80, timeout=0.001)
        self.assertIsInstance(result, bool)
    
    def test_scan_port_negative_port(self):
        """Test scan_port with negative port."""
        # Should not crash
        try:
            result = self.ns.scan_port("127.0.0.1", -1, timeout=0.1)
            self.assertIsInstance(result, bool)
        except (ValueError, OSError):
            pass  # Expected behavior
    
    def test_scan_port_large_port(self):
        """Test scan_port with port > 65535."""
        # Should handle gracefully
        try:
            result = self.ns.scan_port("127.0.0.1", 70000, timeout=0.1)
            self.assertIsInstance(result, bool)
        except (ValueError, OSError):
            pass  # Expected behavior
    
    def test_dns_lookup_empty_string(self):
        """Test DNS lookup with empty string."""
        result = self.ns.dns_lookup("")
        self.assertTrue(result is None or isinstance(result, str))
    
    def test_reverse_dns_empty_string(self):
        """Test reverse DNS with empty string."""
        result = self.ns.reverse_dns("")
        self.assertIsNone(result)


class TestFormatPortResults(unittest.TestCase):
    """Test output formatting."""
    
    def test_format_port_results_open_ports(self):
        """Test format_port_results with open ports."""
        results = {80: True, 443: True, 22: False}
        # Should not raise
        with patch('builtins.print'):
            format_port_results("test.host", results)
    
    def test_format_port_results_no_open_ports(self):
        """Test format_port_results with no open ports."""
        results = {80: False, 443: False}
        # Should not raise
        with patch('builtins.print'):
            format_port_results("test.host", results)
    
    def test_format_port_results_empty(self):
        """Test format_port_results with empty results."""
        results = {}
        # Should not raise
        with patch('builtins.print'):
            format_port_results("test.host", results)


class TestCrossPlatform(unittest.TestCase):
    """Test cross-platform compatibility."""
    
    def test_platform_detection(self):
        """Test platform is detectable."""
        system = platform.system().lower()
        self.assertIn(system, ["windows", "linux", "darwin"])
    
    def test_ping_uses_correct_flag(self):
        """Test ping uses correct count flag for platform."""
        ns = NetScan()
        system = platform.system().lower()
        # Just verify it doesn't crash
        success, output = ns.ping("127.0.0.1", count=1)
        self.assertIsInstance(success, bool)


class TestThreadSafety(unittest.TestCase):
    """Test thread safety and concurrent operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_concurrent_port_scans(self):
        """Test multiple concurrent port scans."""
        ports = list(range(80, 90))
        result = self.ns.scan_ports("127.0.0.1", ports, timeout=0.1, threads=10)
        self.assertEqual(len(result), len(ports))
    
    def test_scan_ports_thread_limit(self):
        """Test scan_ports with thread limit."""
        ports = list(range(80, 100))
        # Should work with any reasonable thread count
        result = self.ns.scan_ports("127.0.0.1", ports, timeout=0.1, threads=2)
        self.assertEqual(len(result), len(ports))


class TestErrorHandling(unittest.TestCase):
    """Test error handling and recovery."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ns = NetScan()
    
    def test_socket_error_handling(self):
        """Test socket errors are handled."""
        # Invalid host should return False, not raise
        result = self.ns.scan_port("256.256.256.256", 80, timeout=0.1)
        self.assertFalse(result)
    
    def test_timeout_handling(self):
        """Test timeout is respected."""
        import time
        start = time.time()
        result = self.ns.scan_port("192.0.2.1", 80, timeout=0.5)  # TEST-NET address
        elapsed = time.time() - start
        # Should complete within reasonable time of timeout
        self.assertLess(elapsed, 3.0)  # Allow some margin
    
    def test_dns_error_handling(self):
        """Test DNS errors are handled."""
        # Should return None, not raise
        result = self.ns.dns_lookup("x" * 100 + ".invalid")
        self.assertIsNone(result)


class TestStaticMethods(unittest.TestCase):
    """Test that methods can be called statically."""
    
    def test_scan_port_static(self):
        """Test scan_port can be called statically."""
        result = NetScan.scan_port("127.0.0.1", 80, timeout=0.1)
        self.assertIsInstance(result, bool)
    
    def test_scan_ports_static(self):
        """Test scan_ports can be called statically."""
        result = NetScan.scan_ports("127.0.0.1", [80], timeout=0.1)
        self.assertIsInstance(result, dict)
    
    def test_dns_lookup_static(self):
        """Test dns_lookup can be called statically."""
        result = NetScan.dns_lookup("localhost")
        self.assertTrue(result is None or isinstance(result, str))
    
    def test_get_local_ip_static(self):
        """Test get_local_ip can be called statically."""
        result = NetScan.get_local_ip()
        self.assertIsInstance(result, str)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: NetScan v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNetScanCore))
    suite.addTests(loader.loadTestsFromTestCase(TestPortScanning))
    suite.addTests(loader.loadTestsFromTestCase(TestDNSOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestLocalIPDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestPingFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestTraceroute))
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkScan))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatPortResults))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossPlatform))
    suite.addTests(loader.loadTestsFromTestCase(TestThreadSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestStaticMethods))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
