# Fire API Documentation

## Overview
Fire provides a RESTful API for programmatic access to network security data and policy management.

## Authentication
All API endpoints require an API key passed in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your_api_key" https://localhost:5000/api/endpoint
```

## Rate Limiting
- **Limit**: 100 requests per 60 seconds
- **Response Code**: 429 Too Many Requests

## Endpoints

### 1. Get All Devices
**Endpoint**: `GET /api/devices`

**Authentication**: Required (API Key)

**Description**: Retrieve list of all monitored devices on the network

**Response**:
```json
[
  {
    "ip": "192.168.1.100",
    "mac": "aa:bb:cc:dd:ee:ff",
    "name": "Device-192.168.1.100",
    "profile": "workstation",
    "trust": "untrusted",
    "risk": 0
  }
]
```

**Example**:
```bash
curl -H "X-API-Key: YOUR_KEY" http://127.0.0.1:5000/api/devices
```

---

### 2. Get Security Violations
**Endpoint**: `GET /api/violations`

**Authentication**: Required (API Key)

**Parameters**:
- `limit` (optional, int): Maximum results (default: 50, max: 500)

**Description**: Retrieve recent security violations

**Response**:
```json
[
  {
    "timestamp": "2026-05-26 14:30:45",
    "ip": "192.168.1.105",
    "mac": "11:22:33:44:55:66",
    "port": 2323,
    "action": "TCP RST & Firewall Block",
    "severity": "medium"
  }
]
```

**Examples**:
```bash
# Get 50 most recent violations
curl -H "X-API-Key: YOUR_KEY" http://127.0.0.1:5000/api/violations

# Get 100 violations
curl -H "X-API-Key: YOUR_KEY" http://127.0.0.1:5000/api/violations?limit=100
```

---

### 3. Whitelist a Device
**Endpoint**: `POST /api/whitelist`

**Authentication**: Required (API Key)

**Headers**: `Content-Type: application/json`

**Request Body**:
```json
{
  "ip": "192.168.1.100",
  "ports": [80, 443, 8080]
}
```

**Description**: Add an IP address to the whitelist

**Response**:
```json
{
  "status": "IP whitelisted"
}
```

**Example**:
```bash
curl -X POST -H "X-API-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"ip":"192.168.1.100","ports":[80,443]}' \
     http://127.0.0.1:5000/api/whitelist
```

---

## Error Responses

### Unauthorized (401)
```json
{
  "error": "Unauthorized"
}
```

### Rate Limited (429)
```json
{
  "error": "Rate limit exceeded"
}
```

### Bad Request (400)
```json
{
  "error": "Invalid IP"
}
```

---

## Python Client Example

```python
import requests
import json

API_KEY = "your_api_key_here"
BASE_URL = "http://127.0.0.1:5000"
HEADERS = {"X-API-Key": API_KEY}

class FireClient:
    def __init__(self, api_key, base_url="http://127.0.0.1:5000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def get_devices(self):
        """Get all monitored devices"""
        response = requests.get(f"{self.base_url}/api/devices", headers=self.headers)
        return response.json()
    
    def get_violations(self, limit=50):
        """Get recent violations"""
        response = requests.get(
            f"{self.base_url}/api/violations?limit={limit}",
            headers=self.headers
        )
        return response.json()
    
    def whitelist_ip(self, ip, ports=[80, 443]):
        """Add IP to whitelist"""
        data = {"ip": ip, "ports": ports}
        response = requests.post(
            f"{self.base_url}/api/whitelist",
            headers=self.headers,
            json=data
        )
        return response.json()

# Usage
client = FireClient("your_api_key_here")

# Get all devices
devices = client.get_devices()
print(f"Found {len(devices)} devices")

# Get violations
violations = client.get_violations(limit=100)
for v in violations:
    print(f"{v['timestamp']}: {v['ip']} port {v['port']} - {v['severity']}")

# Whitelist a device
result = client.whitelist_ip("192.168.1.100", [80, 443])
print(result)
```

---

## Command-Line Examples

### Get all devices (using curl)
```bash
curl -H "X-API-Key: YOUR_KEY" \
     http://127.0.0.1:5000/api/devices | python -m json.tool
```

### Get violations in past 24 hours (using python)
```bash
python -c "
import requests
from datetime import datetime, timedelta

api_key = 'YOUR_KEY'
headers = {'X-API-Key': api_key}
url = 'http://127.0.0.1:5000/api/violations?limit=500'

violations = requests.get(url, headers=headers).json()
for v in violations:
    print(f\"{v['timestamp']} - {v['ip']:15} Port {v['port']:5} {v['severity']}\")
"
```

### Monitor violations in real-time (using python)
```bash
python -c "
import requests
import time

api_key = 'YOUR_KEY'
headers = {'X-API-Key': api_key}
url = 'http://127.0.0.1:5000/api/violations?limit=10'

while True:
    violations = requests.get(url, headers=headers).json()
    print(f\"[{time.ctime()}] Latest {len(violations)} violations\")
    for v in violations[:3]:
        print(f\"  {v['ip']:15} Port {v['port']:5} {v['severity']}\")
    time.sleep(30)
" &
```

---

## Rate Limiting Details

Each client IP is rate-limited to 100 requests per 60-second window.

### Rate Limit Headers
The API includes rate limit information in response headers:
- `X-RateLimit-Limit`: 100
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

---

## Best Practices

1. **Store API Key Securely**: Never commit API keys to version control
2. **Use Environment Variables**: `export FIRE_API_KEY="your_key"`
3. **Implement Retry Logic**: Handle rate limiting with exponential backoff
4. **Monitor API Usage**: Log API calls for audit purposes
5. **Use HTTPS**: Always use HTTPS in production (not http://)

---

## Troubleshooting

### "Unauthorized" Error
- Verify API key is correct
- Check that API key is still active in database
- Ensure key is in `X-API-Key` header (not in body)

### "Rate limit exceeded" Error
- Reduce request frequency
- Implement exponential backoff for retries
- Check if multiple processes are using same API key

### Empty Device List
- Ensure daemon has discovered devices (check logs)
- Network connectivity issues
- Verify scan_interval setting in config

---

## WebSocket Support (Future)
Real-time threat notifications via WebSocket will be added in v2.0

---

## Version History

- **v1.0** (Current): Basic API with device listing, violations, and whitelist
- **v1.1** (Planned): Blacklist endpoint, threat notifications
- **v2.0** (Planned): WebSocket support, policy management API
