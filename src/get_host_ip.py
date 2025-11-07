import socket
import json
import sys
from pathlib import Path

def get_host_info(hostname):
    """Get IP information for a given hostname."""
    info = {
        "hostname": hostname,
        "fqdn": None,
        "ipv4": [],
        "ipv6": []
    }
    
    try:
        # Get FQDN
        info["fqdn"] = socket.getfqdn(hostname)
        
        # Try multiple methods to get all IP addresses
        
        # Method 1: getaddrinfo with unspecified family (gets both IPv4 and IPv6)
        try:
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC)
            for addr in addr_info:
                family = addr[0]
                ip = addr[4][0]
                
                # Remove zone ID from IPv6 addresses (e.g., %eth0)
                if '%' in ip:
                    ip = ip.split('%')[0]
                
                if family == socket.AF_INET and ip not in info["ipv4"]:
                    info["ipv4"].append(ip)
                elif family == socket.AF_INET6 and ip not in info["ipv6"]:
                    info["ipv6"].append(ip)
        except socket.gaierror:
            pass
        
        # Method 2: Explicitly try IPv4
        try:
            ipv4_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
            for addr in ipv4_info:
                ip = addr[4][0]
                if ip not in info["ipv4"]:
                    info["ipv4"].append(ip)
        except socket.gaierror:
            pass
        
        # Method 3: Explicitly try IPv6
        try:
            ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            for addr in ipv6_info:
                ip = addr[4][0]
                # Remove zone ID from IPv6 addresses
                if '%' in ip:
                    ip = ip.split('%')[0]
                if ip not in info["ipv6"]:
                    info["ipv6"].append(ip)
        except socket.gaierror:
            pass
        
        # If we still have no results, raise an error
        if not info["ipv4"] and not info["ipv6"]:
            raise socket.gaierror("No addresses found")
                
    except socket.gaierror as e:
        info["error"] = f"DNS lookup failed: {str(e)}"
    except Exception as e:
        info["error"] = f"Error: {str(e)}"
    
    return info

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_host_ip.py <hostnames_file>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    results = []
    
    # Read hostnames from file
    with open(input_file, 'r') as f:
        hostnames = [line.strip() for line in f if line.strip()]
    
    # Process each hostname
    for hostname in hostnames:
        print(f"Processing: {hostname}")
        results.append(get_host_info(hostname))
    
    # Generate output filename in results directory
    output_dir = Path(__file__).parent.parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{input_file.stem}_results.json"
    
    # Write results to JSON
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
