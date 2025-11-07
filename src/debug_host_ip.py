import socket
import sys

def debug_host_info(hostname):
    """Debug version - shows detailed DNS resolution information."""
    print(f"\n{'='*60}")
    print(f"Hostname: {hostname}")
    print(f"{'='*60}")
    
    try:
        # Get FQDN
        fqdn = socket.getfqdn(hostname)
        print(f"FQDN: {fqdn}")
        
        # Try AF_UNSPEC (both IPv4 and IPv6)
        print(f"\n--- AF_UNSPEC (All families) ---")
        try:
            results = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC)
            for i, addr in enumerate(results, 1):
                family_name = "IPv4" if addr[0] == socket.AF_INET else "IPv6" if addr[0] == socket.AF_INET6 else "Other"
                print(f"{i}. Family: {family_name}, Address: {addr[4][0]}")
        except socket.gaierror as e:
            print(f"Error: {e}")
        
        # Try AF_INET (IPv4 only)
        print(f"\n--- AF_INET (IPv4 only) ---")
        try:
            results = socket.getaddrinfo(hostname, None, socket.AF_INET)
            for i, addr in enumerate(results, 1):
                print(f"{i}. Address: {addr[4][0]}")
        except socket.gaierror as e:
            print(f"Error: {e}")
        
        # Try AF_INET6 (IPv6 only)
        print(f"\n--- AF_INET6 (IPv6 only) ---")
        try:
            results = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            for i, addr in enumerate(results, 1):
                print(f"{i}. Address: {addr[4][0]}")
        except socket.gaierror as e:
            print(f"Error: {e}")
        
        # Try gethostbyname (legacy IPv4)
        print(f"\n--- gethostbyname (legacy IPv4) ---")
        try:
            ip = socket.gethostbyname(hostname)
            print(f"Address: {ip}")
        except socket.gaierror as e:
            print(f"Error: {e}")
        
        # Try gethostbyname_ex (extended IPv4)
        print(f"\n--- gethostbyname_ex (extended IPv4) ---")
        try:
            name, aliases, ips = socket.gethostbyname_ex(hostname)
            print(f"Name: {name}")
            print(f"Aliases: {aliases}")
            print(f"Addresses: {ips}")
        except socket.gaierror as e:
            print(f"Error: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_host_ip.py <hostname>")
        print("\nTrying with some examples...")
        hostnames = ["localhost", "google.com"]
    else:
        hostnames = sys.argv[1:]
    
    for hostname in hostnames:
        debug_host_info(hostname)
    
    print(f"\n{'='*60}")
