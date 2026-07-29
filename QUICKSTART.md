# 🔥 Fire - Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Setup Tool
```bash
python setup.py
```

Select option **1** to verify all requirements are installed.

### Step 3: Initialize Database
```bash
python setup.py
```

Select option **2** to initialize the database with default tables.

### Step 4: Change Default Password (IMPORTANT!)
```bash
python setup.py
```

Select option **3** to change the admin password from `Fire@2026!` to a secure password.

### Step 5: Generate API Key (Optional)
```bash
python setup.py
```

Select option **4** to generate an API key for programmatic access.

---

## Running Fire

### Method 1: Direct Python
```bash
python Fire.py
```

### Method 2: Using Setup Tool
```bash
python setup.py
```

Select option **7** to start the service.

**Dashboard URL**: http://127.0.0.1:5000

---

## First Login

1. Navigate to **http://127.0.0.1:5000**
2. Enter credentials:
   - **Username**: admin
   - **Password**: (your new password)
3. Click **Login**

---

## Dashboard Overview

### Statistics Panel
- **Monitored Devices**: Total devices discovered on network
- **Recent Violations**: Number of policy violations recorded
- **Active Threats**: Number of unresolved threat events

### Security Violations Table
Shows unauthorized port access attempts:
- Timestamp
- Device IP
- MAC Address
- Port number
- Action taken
- Severity level

### Threats Table
Shows detected suspicious activities:
- Port scanning attempts
- DDoS patterns
- Anomalous behavior

---

## Configuration

Edit `config.json` to customize:

```json
{
  "network": {
    "subnet": "192.168.1.0/24",      # Your network range
    "interface": "Wi-Fi",             # Your network interface
    "scan_interval": 60               # Scan every 60 seconds
  },
  "security": {
    "enable_firewall_blocking": true, # Block via OS firewall
    "enable_tcp_reset": true,         # Send TCP RST packets
    "rate_limit": 100,                # API rate limit
    "rate_limit_window": 60           # Per 60 seconds
  }
}
```

---

## API Usage

### 1. Get Your API Key
```bash
python setup.py
# Select option 4
```

### 2. View Devices
```bash
curl -H "X-API-Key: YOUR_KEY" http://127.0.0.1:5000/api/devices
```

### 3. View Recent Violations
```bash
curl -H "X-API-Key: YOUR_KEY" http://127.0.0.1:5000/api/violations?limit=50
```

### 4. Whitelist a Device
```bash
curl -X POST -H "X-API-Key: YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"ip":"192.168.1.100","ports":[80,443]}' \
     http://127.0.0.1:5000/api/whitelist
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

---

## Common Tasks

### View Security Logs
```bash
tail -f fire_security.log
```

### View Recent Violations
```bash
python setup.py
# Select option 5
```

### View Monitored Devices
```bash
python setup.py
# Select option 6
```

### Monitor in Real-time
```bash
python -c "
import requests
import time

key = 'YOUR_API_KEY'
headers = {'X-API-Key': key}

while True:
    violations = requests.get(
        'http://127.0.0.1:5000/api/violations?limit=10',
        headers=headers
    ).json()
    
    print(f'[{time.ctime()}] {len(violations)} recent violations')
    for v in violations[:3]:
        print(f\"  {v['ip']:15} Port {v['port']:5} {v['severity']}\")
    
    time.sleep(30)
"
```

---

## Troubleshooting

### Dashboard Not Loading?
```bash
# Check if Fire is running
netstat -an | findstr 5000

# Check for errors
tail -f fire_security.log

# Verify network interface name
ipconfig
# Update 'interface' in Fire.py or config.json
```

### No Devices Discovered?
```bash
# Check network connectivity
ping 8.8.8.8

# Verify subnet configuration
ipconfig /all

# Check nmap installation
nmap --version

# Review logs
tail -f fire_security.log
```

### Violations Not Being Blocked?
```bash
# Run as Administrator (required for firewall rules)
# Right-click Command Prompt > Run as Administrator

# Check Windows Firewall rules
netsh advfirewall firewall show rule name=Fire*

# Check logs for errors
tail -f fire_security.log
```

---

## Security Best Practices

1. **Change Default Password Immediately**
   ```bash
   python setup.py
   # Option 3
   ```

2. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Avoid dictionary words

3. **Protect API Keys**
   - Never share API keys
   - Store in environment variables
   - Rotate regularly
   - Disable unused keys

4. **Monitor Access Logs**
   ```bash
   grep "LOGIN\|LOGOUT\|WHITELIST" fire_security.log
   ```

5. **Regular Backups**
   ```bash
   # Backup database weekly
   copy security_log.db security_log.db.backup
   ```

6. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## Performance Tuning

### For Small Networks (< 50 devices)
```json
{
  "scan_interval": 120,        # Scan every 2 minutes
  "port_scan_threshold": 15,   # Higher threshold
  "ddos_window": 120           # Longer window
}
```

### For Large Networks (> 200 devices)
```json
{
  "scan_interval": 30,         # Scan every 30 seconds
  "port_scan_threshold": 8,    # Lower threshold
  "ddos_window": 30            # Shorter window
}
```

---

## Understanding Threat Levels

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Severe threat detected | Immediate investigation |
| **HIGH** | Suspicious activity | Verify and investigate |
| **MEDIUM** | Policy violation | Log and monitor |
| **LOW** | Minor anomaly | Log for audit trail |

---

## Getting Help

1. **Check logs**: `tail -f fire_security.log`
2. **Review README**: [README.md](README.md)
3. **API docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. **Changes**: [CHANGELOG.md](CHANGELOG.md)

---

## Next Steps

- [ ] Install Fire
- [ ] Configure network settings
- [ ] Change admin password
- [ ] Generate API key
- [ ] View dashboard
- [ ] Test API endpoints
- [ ] Monitor for violations
- [ ] Set up backups

---

🎉 **Fire is now ready to protect your network!**

Remember: **Effective security requires regular monitoring and updates.**
