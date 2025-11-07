import unittest
import sys
import socket
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from get_host_ip import get_host_info

try:
    import dns.resolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False


class TestGetHostInfo(unittest.TestCase):
    """Test cases for get_host_info function."""
    
    def test_localhost(self):
        """Test resolving localhost."""
        result = get_host_info("localhost")
        
        self.assertEqual(result["hostname"], "localhost")
        self.assertIsNotNone(result["fqdn"])
        self.assertIsInstance(result["ipv4"], list)
        self.assertIsInstance(result["ipv6"], list)
        
        # localhost should have at least one IP address
        self.assertTrue(len(result["ipv4"]) > 0 or len(result["ipv6"]) > 0)
        
        # Check if 127.0.0.1 is in IPv4 addresses
        self.assertIn("127.0.0.1", result["ipv4"])
    
    def test_loopback_ipv6(self):
        """Test resolving IPv6 loopback."""
        result = get_host_info("::1")
        
        self.assertIsInstance(result["ipv6"], list)
        # IPv6 loopback should be present
        self.assertTrue(any("::1" in ip for ip in result["ipv6"]))
    
    def test_google_dns(self):
        """Test resolving google.com."""
        result = get_host_info("google.com")
        
        self.assertEqual(result["hostname"], "google.com")
        self.assertIsNotNone(result["fqdn"])
        
        # Google should have at least IPv4 (IPv6 depends on network)
        self.assertTrue(len(result["ipv4"]) > 0 or len(result["ipv6"]) > 0)
        
        # Verify IPv4 format
        for ip in result["ipv4"]:
            self.assertRegex(ip, r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        
        # Verify IPv6 format if present
        for ip in result["ipv6"]:
            self.assertIn(':', ip)
    
    def test_invalid_hostname(self):
        """Test handling of invalid hostname."""
        result = get_host_info("this-hostname-does-not-exist-12345.invalid")
        
        self.assertIn("error", result)
        self.assertIn("DNS lookup failed", result["error"])
    
    def test_empty_hostname(self):
        """Test handling of empty hostname."""
        result = get_host_info("")
        
        # Empty hostname should either resolve or produce an error
        self.assertTrue("error" in result or result["fqdn"] is not None)
    
    def test_ipv4_address_input(self):
        """Test resolving an IPv4 address directly."""
        result = get_host_info("8.8.8.8")
        
        self.assertEqual(result["hostname"], "8.8.8.8")
        self.assertIn("8.8.8.8", result["ipv4"])
    
    def test_result_structure(self):
        """Test that result has correct structure."""
        result = get_host_info("localhost")
        
        # Check all required keys are present
        required_keys = ["hostname", "fqdn", "ipv4", "ipv6"]
        for key in required_keys:
            self.assertIn(key, result)
        
        # Check types
        self.assertIsInstance(result["hostname"], str)
        self.assertIsInstance(result["ipv4"], list)
        self.assertIsInstance(result["ipv6"], list)
    
    def test_no_duplicate_ips(self):
        """Test that IP addresses are not duplicated."""
        result = get_host_info("localhost")
        
        # Check IPv4 for duplicates
        self.assertEqual(len(result["ipv4"]), len(set(result["ipv4"])))
        
        # Check IPv6 for duplicates
        self.assertEqual(len(result["ipv6"]), len(set(result["ipv6"])))
    
    def test_cloudflare_dns(self):
        """Test resolving cloudflare.com."""
        result = get_host_info("cloudflare.com")
        
        self.assertEqual(result["hostname"], "cloudflare.com")
        self.assertIsNotNone(result["fqdn"])
        
        # Should have at least one IP address
        self.assertTrue(len(result["ipv4"]) > 0 or len(result["ipv6"]) > 0)


class TestIPAddressValidation(unittest.TestCase):
    """Test cases for IP address validation."""
    
    def test_ipv4_format(self):
        """Test that IPv4 addresses have correct format."""
        result = get_host_info("localhost")
        
        for ip in result["ipv4"]:
            # Check format
            parts = ip.split('.')
            self.assertEqual(len(parts), 4)
            
            # Each part should be a number between 0-255
            for part in parts:
                num = int(part)
                self.assertGreaterEqual(num, 0)
                self.assertLessEqual(num, 255)
    
    def test_ipv6_format(self):
        """Test that IPv6 addresses contain colons."""
        result = get_host_info("::1")
        
        for ip in result["ipv6"]:
            # IPv6 addresses should contain colons
            self.assertIn(':', ip)
    
    @unittest.skipIf(not HAS_DNSPYTHON, "dnspython not installed")
    def test_dns_query_google(self):
        """Test direct DNS query for google.com."""
        result = get_host_info("google.com")
        
        # Should get results via DNS query
        self.assertTrue(len(result["ipv4"]) > 0 or len(result["ipv6"]) > 0)
        self.assertNotIn("error", result)
    
    def test_no_zone_id_in_ipv6(self):
        """Test that zone IDs are stripped from IPv6 addresses."""
        result = get_host_info("localhost")
        
        # IPv6 addresses should not contain % (zone ID)
        for ip in result["ipv6"]:
            self.assertNotIn('%', ip, "IPv6 address should not contain zone ID")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
