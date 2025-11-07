# Host IP Lookup Tool

A Python script to resolve hostnames and retrieve both IPv4 and IPv6 addresses.

## Project Structure

```
host-ip/
├── src/
│   └── get_host_ip.py      # Main script
├── tests/
│   └── test_get_host_ip.py # Test cases
├── results/                 # Output JSON files
├── hostnames.txt           # Input file with hostnames
└── README.md
```

## Features

- Resolves hostnames to IP addresses using direct DNS queries (like nslookup)
- Supports both IPv4 (A records) and IPv6 (AAAA records)
- Returns FQDN (Fully Qualified Domain Name)
- Outputs results in JSON format
- Handles DNS lookup errors gracefully
- Falls back to socket resolution if DNS query fails

## Usage

```bash
python src/get_host_ip.py hostnames.txt
```

### Input Format

Create a `hostnames.txt` file with one hostname per line:

```
google.com
localhost
github.com
```

### Output Format

Results are saved as JSON in the `results/` directory:

```json
[
  {
    "hostname": "google.com",
    "fqdn": "google.com",
    "ipv4": ["142.250.185.46"],
    "ipv6": ["2607:f8b0:4004:c07::71"]
  }
]
```

## Running Tests

Run the test suite:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest tests/test_get_host_ip.py -v
```

## Troubleshooting

If IPv6 addresses are not being captured:

1. Test DNS resolution directly:
```bash
python src/test_dns.py <hostname>
```

2. Compare with nslookup:
```bash
nslookup <hostname>
```

3. Ensure dnspython is installed:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.6+
- dnspython (for direct DNS queries like nslookup)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/atulksin/host-ip.git
cd host-ip
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## License

MIT
