"""
Quick test script to compare nslookup-style DNS queries vs socket resolution
"""
import sys

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False
    print("Warning: dnspython not installed. Install with: pip install dnspython")

import socket

def test_hostname(hostname):
    print(f"\n{'='*70}")
    print(f"Testing: {hostname}")
    print(f"{'='*70}")
    
    # DNS Query (like nslookup)
    if HAS_DNS:
        print("\n--- Direct DNS Query (like nslookup) ---")
        
        print("\nIPv4 (A records):")
        try:
            answers = dns.resolver.resolve(hostname, 'A')
            for rdata in answers:
                print(f"  {rdata}")
        except Exception as e:
            print(f"  No A records found: {e}")
        
        print("\nIPv6 (AAAA records):")
        try:
            answers = dns.resolver.resolve(hostname, 'AAAA')
            for rdata in answers:
                print(f"  {rdata}")
        except Exception as e:
            print(f"  No AAAA records found: {e}")
    
    # Socket getaddrinfo
    print("\n--- Socket getaddrinfo (Python default) ---")
    
    print("\nIPv4:")
    try:
        results = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for addr in results:
            print(f"  {addr[4][0]}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\nIPv6:")
    try:
        results = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        for addr in results:
            print(f"  {addr[4][0]}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        hostnames = sys.argv[1:]
    else:
        print("Usage: python test_dns.py <hostname1> [hostname2] ...")
        print("\nTesting with example hostnames:")
        hostnames = ["google.com", "localhost"]
    
    for hostname in hostnames:
        test_hostname(hostname)
    
    print(f"\n{'='*70}\n")
