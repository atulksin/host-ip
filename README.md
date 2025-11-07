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

- Resolves hostnames to IP addresses
- Supports both IPv4 and IPv6
- Returns FQDN (Fully Qualified Domain Name)
- Outputs results in JSON format
- Handles DNS lookup errors gracefully

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
python -m unittest tests/test_get_host_ip.py
```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## License

MIT
