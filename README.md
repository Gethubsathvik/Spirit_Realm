# 🔥 Spirit Realm - Advanced Network Security Enforcement System

![Spirit Realm Logo](https://img.shields.io/badge/Spirit_Realm-Security-red?style=for-the-badge&logo=fire)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Go](https://img.shields.io/badge/Go-1.22%2B-00ADD8?style=for-the-badge&logo=go)
![C](https://img.shields.io/badge/C-Standard-A8B9CC?style=for-the-badge&logo=c)
![Node.js](https://img.shields.io/badge/Node.js-18.x%2B-339933?style=for-the-badge&logo=node.js)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge&logo=flask)
![Scapy](https://img.shields.io/badge/Scapy-Packet%20Crafting-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🎯 Overview

Spirit Realm is an autonomous network security enforcement system that monitors your network for unauthorized device behavior and enforces security policies automatically. It combines advanced threat detection, device profiling, and automated response mechanisms.

### 🚀 Key Capabilities

- 🛡️ **Autonomous Threat Detection** — Port scanning, DDoS patterns, malware signatures
- 📊 **Device Profiling** — Automatic device type identification and risk scoring
- 🔐 **User Authentication** — Secure login with password hashing and session management
- 📡 **Deep Packet Inspection** — Real-time packet analysis and filtering
- 🚫 **Automated Enforcement** — TCP RST injection + OS firewall blocking
- 📈 **Multi-Language API** — Full programmatic access with RESTful interfaces (Python, Go, Node.js clients)
- 🌐 **Cross-Platform** — Works on Windows, macOS, Linux, and Android
- ⚡ **Polyglot Architecture** — Combines Python, Go, C, and Node.js for optimal performance

---
## 🏗️ Architecture 
Spirit Realm follows a **Model-View-Controller (MVC)** pattern with a **service layer** separating business logic from routing, enhanced with **microservices** for performance-critical components:
 ---

## 📁 File Structure

```
Spirit Realm/
├── spirit_realm.py             # 🎬 Main orchestrator (Python)
├── setup.py                    # 🔧 Interactive setup & management tool
├── config.json                 # ⚙️ Configuration template
├── requirements.txt            # 📦 Python dependencies
├── go.mod                      # 🐹 Go module definition
├── go.sum                      # 🐹 Go module checksums
├── package.json                # 📦 Node.js dependencies (root)
├── README.md                   # 📖 This file
├── API_DOCUMENTATION.md        # 📚 Complete API reference
├── QUICKSTART.md               # 🚀 Quick start guide
├── CHANGELOG.md                # 📝 Version history
├── LICENSE                     # 📄 MIT License
├── spirit_security.log         # 📝 Runtime log (auto-created)
├── security_log.db             # 💾 SQLite database (auto-created)
│
├── app/
│   ├── __init__.py
│   ├── config.py               # 📋 Centralized configuration
│   │
│   ├── core/                   # 🧠 Shared services (Model layer)
│   │   ├── __init__.py
│   │   ├── database.py         #   SQLite data access
│   │   ├── firewall_os.py      #   OS firewall integration
│   │   └── logger.py           #   Centralized logging
│   │
│   ├── services/               # ⚡ Cross-language services
│   │   ├── __init__.py
│   │   ├── packet_service/     #   High-performance packet processing
│   │   │   ├── go.mod          #   Go module definition
│   │   │   ├── main.go         #   Go service entry point
│   │   │   ├── packet.go       #   Packet structures & handling
│   │   │   └── handler.go      #   gRPC/HTTP handlers
│   │   │
│   │   ├── packet_inspector/   #   Low-level packet inspection (C)
│   │   │   ├── packet_service.h    #   Header file
│   │   │   ├── packet_service.c    #   Implementation
│   │   │   └── Makefile          #   Build instructions
│   │   │
│   │   └── shared/             #   Shared interfaces
│   │       └── packet_types.go #   Common data structures
│   │
│   ├── features/               # 🎯 Feature modules
│   │   ├── __init__.py
│   │   ├── auth/               #   🔐 Authentication feature
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       #     Controller
│   │   │   └── services.py     #     Service
│   │   │
│   │   ├── firewall/           #   🛡️ Firewall feature
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       #     Controller
│   │   │   ├── services.py     #     Service
│   │   │   ├── engine.py       #     Model (firewall engine)
│   │   │   └── sniffer.py      #     Service (packet inspection interface)
│   │   │
│   │   └── devices/            #   📡 Device management feature
│   │       ├── __init__.py
│   │       ├── routes.py       #     Controller
│   │       ├── services.py     #     Service
│   │       └── scanner.py      #     Model (discovery + scanning)
│   │
│   └── dashboard/              # 🖥️ Frontend dashboard (Node.js/React)
│       ├── package.json
│       ├── src/
│       │   ├── index.js
│   │   ├── components/
│   │   ├── services/
│   │   └── public/
│       │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│
└── docker/
    ├── Dockerfile.python       # Python service container
    ├── Dockerfile.go           # Go packet service container
    ├── Dockerfile.node         # Node.js dashboard container
    └── docker-compose.yml      # Orchestration
```


**How MVC works in Spirit Realm:**

| Layer | Component | Responsibility |
|-------|-----------|---------------|
| **Model** | `config.py`, `database.py`, `engine.py`, `scanner.py`, `packet_service.c` | Data structures, DB schema, firewall rules, device profiles, threat detection algorithms, packet processing |
| **View** | HTML templates in `routes.py`, `dashboard/public/` | Dashboard UI, login page, API JSON responses |
| **Controller** | `routes.py` files (blueprints) | HTTP request handling, session management, input validation |
| **Service** | `services.py` files, `packet_service.go`, `packet_service.c` | Business logic: enforcement, audit logging, policy evaluation, high-speed packet processing |
| **Microservice** | `packet_service.go` | Independent high-throughput packet processing service |

---

### 🧩 Feature-Based Structure

Spirit Realm is organized as **feature modules**, each self-contained with its own routes, services, and models:

| Feature | Directory | Routes | Services | Models |
|---------|-----------|--------|----------|--------|
| 🔐 **Authentication** | `app/features/auth/` | `routes.py` | `services.py` | Users, API Keys, Sessions |
| 🛡️ **Firewall** | `app/features/firewall/` | `routes.py` | `services.py` | `engine.py`, `sniffer.py` | Rules, Threats, Violations |
| 📡 **Device Management** | `app/features/devices/` | `routes.py` | `services.py` | `scanner.py` | Devices, Profiles, Trust Levels |
| 📊 **Dashboard** | `app/dashboard/` | N/A | Server.js | Frontend assets |
| ⚡ **Packet Processing** | `app/services/` | N/A | `packet_service.go`, `packet_service.c` | Packet structures, filters |

Each feature module is a **self-contained unit** that can be developed, tested, and scaled independently.

---

### 🏛️ Microservices Architecture

Spirit Realm is designed with a **microservices-inspired architecture** where each component can be extracted into an independent service:

```
┌─────────────────────────────────────────────────────────────┐
│                    Spirit Realm Platform                    │
├─────────────┬──────────────┬──────────────┬────────────────┤
│  🔐 Auth    │  🛡️ Firewall │  📡 Scanner  │  📊 Dashboard  │
│  Service    │  Service     │  Service     │  Service       │
│             │              │              │                │
│  - Login    │  - Packet    │  - ARP       │  - UI          │
│  - API Key  │    Inspection│    Discovery │  - Stats       │
│  - Session  │  - SYN Flood │  - Port      │  - Violations  │
│  - Audit    │  - DDoS      │    Scan      │  - Threats     │
│  - Rate     │  - Policy    │  - Device    │  - Firewall    │
│    Limit    │    Enforce   │    Profile   │    Rules       │
├─────────────┼──────────────┼──────────────┼────────────────┤
│  Shared: SQLite DB │ Shared: Config │ Shared: Logger      │
└─────────────────────────────────────────────────────────────┘
```

**Microservices readiness:**
- ✅ Each feature module has its own `routes.py` and `services.py`
- ✅ Shared services (`database`, `logger`, `firewall_os`) are in `app/core/`
- ✅ Configuration is centralized in `app/config.py` and `config.json`
- ✅ Blueprints enable independent registration of feature modules
- ✅ API-first design — all features accessible via REST endpoints
- ✅ gRPC service for high-performance packet processing (Go)

**To extract into true microservices:**
1. Containerize each feature module (Docker)
2. Replace SQLite with a shared database (PostgreSQL/MySQL)
3. Use message queues (RabbitMQ/Redis) for inter-service communication
4. Add API gateway for routing and rate limiting
5. Deploy each service independently

---

## 💻 Cross-Platform Support

Spirit Realm works on **Windows**, **macOS**, **Linux**, and **Android** with platform-specific handling:

### 🪟 Windows

| Component | Implementation |
|-----------|---------------|
| Firewall | `netsh advfirewall` (built-in) |
| Packet Capture | Npcap + Scapy |
| Interface | `"Wi-Fi"` or `"Ethernet"` |
| Privileges | Run as Administrator |
| Go Build | `go build -o spirit_packet.exe` |
| C Build | `gcc -shared -o packet_service.dll packet_service.c` |

### 🍎 macOS

| Component | Implementation |
|-----------|---------------|
| Firewall | `pfctl` (packet filter) or `socketfilterfw` |
| Packet Capture | ApplePCap + Scapy |
| Interface | `"en0"`, `"en1"`, etc. |
| Privileges | `sudo` required |
| Go Build | `GOOS=darwin go build -o spirit_packet` |
| C Build | `gcc -shared -o packet_service.dylib packet_service.c` |

### 🐧 Linux

| Component | Implementation |
|-----------|---------------|
| Firewall | `iptables` (legacy) or `nftables` |
| Packet Capture | libpcap + Scapy |
| Interface | `"eth0"`, `"wlan0"`, etc. |
| Privileges | `sudo` required |
| Go Build | `GOOS=linux go build -o spirit_packet` |
| C Build | `gcc -shared -o packet_service.so -fPIC packet_service.c` |

### 📱 Android (Termux)

| Component | Implementation |
|-----------|---------------|
| Firewall | `iptables` via `su` (root) |
| Packet Capture | `tcpdump` + Scapy (limited) |
| Interface | `"wlan0"` or `"eth0"` |
| Privileges | Root access required |
| Go Build | `GOOS=android GOARCH=arm64 go build -o spirit_packet` |
| C Build | `aarch64-linux-android-gcc -shared -o libpacket_service.so packet_service.c` |

### 🔧 Auto-Detection

Spirit Realm automatically detects your platform and sets the default network interface:

```python
# app/config.py
INTERFACE = os.getenv('INTERFACE', None) or Config.get_default_interface()
# Windows → "Wi-Fi"    macOS → "en0"    Linux → "eth0"    Android → "eth0"
```

You can override the interface via environment variable:
```bash
export INTERFACE="wlan0"   # Linux/macOS/Android
set INTERFACE=Wi-Fi        # Windows
```

---

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- Go 1.22+ (for packet processing microservice)
- GCC compiler (for C packet inspection module)
- Node.js 18.x+ (for dashboard frontend)
- pip
- Root/Administrator privileges (for firewall rules and packet capture)

### ⚡ Installation

```bash
# 1. Clone or navigate to the project
cd "Spirit Realm"

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Go dependencies (for packet service)
cd app/services/packet_service && go mod download && cd ../..

# 4. Build C packet inspection module
cd app/services/packet_inspector && make && cd ../..

# 5. Install Node.js dependencies (for dashboard)
cd app/dashboard && npm install && cd ../..

# 6. Run the setup tool (optional)
python setup.py
```

### ▶️ Running Spirit Realm

**Method 1: Direct execution**
```bash
# Windows (Run as Administrator)
python spirit_realm.py

# macOS / Linux
sudo python3 spirit_realm.py
```

**Method 2: Using the setup tool**
```bash
python setup.py
# Select option 7: Start Spirit Realm Service
```

**Method 3: Docker (recommended for production)**
```bash
docker-compose up --build
```

**Method 4: With custom settings**
```bash
# Override subnet and interface
set SUBNET=10.0.0.0/24
set INTERFACE=Ethernet
python spirit_realm.py
```

### 🌐 Access the Dashboard

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

**Default Credentials:**
- Username: `admin`
- Password: `Spirit@2026!`

> ⚠️ **IMPORTANT**: Change the default password immediately after first login!

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/devices` | List all monitored devices | API Key |
| `GET` | `/api/violations?limit=50` | Get security violations | API Key |
| `POST` | `/api/whitelist` | Add device to whitelist | API Key |
| `GET` | `/api/firewall/stats` | Get firewall statistics | API Key |
| `GET` | `/api/firewall/rules` | List all firewall rules | API Key |
| `POST` | `/api/firewall/rule` | Add a firewall rule | API Key |
| `GET` | `/api/firewall/blocked-ips` | List blocked IPs | API Key |
| `POST` | `/api/firewall/block-ip` | Manually block an IP | API Key |
| `GET` | `/api/firewall/ip-reputation?ip=X.X.X.X` | Get IP reputation | API Key |
| `POST` | `/api/firewall/bandwidth-limit` | Set bandwidth limit | API Key |
| `GET` | `/api/firewall/ddos-events` | Get DDoS events | API Key |
| `GET` | `/api/dashboard/stats` | Get real-time dashboard stats | API Key |

---

## 📊 Device Profiles

Spirit Realm automatically identifies and manages devices:

| Profile | Common Devices | Allowed Ports | Risk Level |
|---------|----------------|---------------|-----------|
| default | Unknown devices | 80, 443 | Medium |
| router | Network routers | 80, 443, 22, 53 | High |
| camera | IP cameras | 80, 443, 8080 | Medium |
| printer | Network printers | 80, 443, 9100 | Low |
| workstation | Windows PCs | 80, 443, 445, 3389 | High |
| nas | Network storage | 80, 443, 445, 22 | High |

---

## 🔍 Threat Detection

| Threat Type | Detection Criteria | Severity | Action |
|-------------|-------------------|----------|--------|
| Port Scanning | 10+ ports in 5 minutes | HIGH | Log + Block |
| DDoS Pattern | 20+ events in 60 seconds | CRITICAL | Log + Block + TCP RST |
| SYN Flood | 100+ SYN packets in 10s | CRITICAL | Block + TCP RST |
| Malware Signature | Known patterns in payload | CRITICAL | Block + Log |
| DNS Amplification | UDP > 512 bytes on port 53 | HIGH | Log + Reputation |
| Port Sweep | Scanning >20 ports in 60s | HIGH | Log + Rate Limit |
| Fragmentation Attack | Invalid IP fragments | MEDIUM | Log + Drop |

---

---

## 🔧 Configuration

Edit `config.json` to customize:

```json
{
  "network": {
    "subnet": "192.168.1.0/24",
    "interface": "Wi-Fi",
    "scan_interval": 60,
    "packet_service_enabled": true
  },
  "security": {
    "enable_firewall_blocking": true,
    "enable_tcp_reset": true,
    "rate_limit": 100,
    "rate_limit_window": 60,
    "enable_prompt_engine": true
  },
  "services": {
    "packet_service": {
      "host": "127.0.0.1",
      "port": 50051,
      "protocol": "grpc",
      "max_workers": 4
    }
  },
  "dashboard": {
    "host": "127.0.0.1",
    "port": 5000,
    "refresh_interval": 5000,
    "theme": "dark"
  }
}
```

Or use environment variables:
```bash
export SUBNET="10.0.0.0/24"
export INTERFACE="eth0"
export PACKET_SERVICE_PORT="50051"
export DASHBOARD_HOST="0.0.0.0"
export DASHBOARD_PORT="8080"
export DEBUG="true"
```

---

## 📈 Performance

- Scans every 60 seconds (configurable)
- Supports up to 254 devices per subnet
- Stores complete history for analysis
- **Go packet service**: Processes 100k+ packets/second
- **C inspection module**: Sub-microsecond packet analysis
- Minimal resource usage with efficient threat detection
- Rate limiting: 100 requests per 60 seconds per IP
- Horizontal scaling via microservices

---

## 🔮 Future Enhancements

- 📧 Email/SMS alerts for critical threats
- 🤖 Machine learning-based anomaly detection (TensorFlow/PyTorch)
- 🔍 Deep Packet Inspection (DPI) with YARA rules
- 📋 Custom firewall rule templates (JSON/YAML)
- 🌐 Multi-subnet support with VLAN tagging
- 🖥️ WebSocket-based real-time dashboard updates
- 💾 Automated backup and disaster recovery
- 🔗 SIEM integration (Splunk ELK, Datadog, etc.)
- 📊 Prometheus/Grafana metrics integration
- 🔐 HashiCorp Vault integration for secret management
- ☁️ Kubernetes deployment manifests
- 🧪 Comprehensive test suite (unit, integration, chaos)

---

## 🛠️ Troubleshooting

### Dashboard not loading?
```bash
# Check if service is running
netstat -an | findstr 5000    # Windows
ss -tlnp | grep 5000          # Linux/macOS

# Check container status (if using Docker)
docker-compose ps

# Review logs
tail -f spirit_security.log
```

### Packet service not responding?
```bash
# Check Go service
netstat -an | findstr 50051   # Windows
ss -tlnp | grep 50051         # Linux/macOS

# Test gRPC connection
grpcurl -plaintext localhost:50051 list

# Check Go service logs
journalctl -u spirit-packet-service  # Linux
```

### C module not loading?
```bash
# Verify shared library exists
ls -la app/services/packet_inspector/

# Check for missing dependencies
ldd app/services/packet_inspector/packet_service.so  # Linux
otool -L app/services/packet_inspector/packet_service.dylib  # macOS
```

### Permission denied on Linux/macOS?
```bash
# Run with appropriate privileges
sudo python3 spirit_realm.py

# Or set capabilities for non-root packet capture
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# For Go service
sudo setcap cap_net_raw,cap_net_admin=eip ./app/services/packet_service/main
```

### Build issues?
```bash
# Go build problems
cd app/services/packet_service && go build -v

# C compilation problems
cd app/services/packet_inspector && make clean && make

# Node.js build problems
cd app/dashboard && npm run build
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file — overview, architecture, quick start |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete REST & gRPC API reference with examples |
| [QUICKSTART.md](QUICKSTART.md) | Step-by-step setup guide for all platforms |
| [CHANGELOG.md](CHANGELOG.md) | Version history and feature changes |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detailed architecture decisions |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contribution guidelines and development setup |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment strategies |
| [SECURITY.md](SECURITY.md) | Security best practices and threat model |

---

## ⚖️ License & Warning

Spirit Realm is provided as-is for authorized network security purposes only.

**MIT License**
Copyright (c) 2026 Spirit Realm Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

---

**Usage Authorization:**
- ✅ Use on networks you own or administer
- ✅ Use with explicit written permission from network owner
- ✅ Use for authorized security testing and monitoring
- ❌ Do not use for unauthorized surveillance or monitoring
- ❌ Comply with all local, national, and international laws
- ❌ Respect privacy rights and data protection regulations

---

## 💡 Contributing

Spirit Realm follows a **polyglot microservices** architecture. To contribute:

### Adding a New Feature (Python)
1. Create a new feature directory under `app/features/`
2. Add `routes.py` (controller), `services.py` (business logic), and model files
3. Register the blueprint in `spirit_realm.py`
4. Add database tables in `app/core/database.py`
5. Update API documentation

### Adding a New Service (Go)
1. Create service directory under `app/services/`
2. Implement Go service with proper logging and error handling
3. Add protobuf definitions if using gRPC
4. Update `go.mod` with dependencies
5. Add health check and metrics endpoints
6. Create Dockerfile for containerization

### Adding a Performance Module (C)
1. Create module under `app/services/packet_inspector/`
2. Implement header file with public functions for the performance-critical component
3. Create a Python wrapper using ctypes/cffi
4. Add build instructions to Makefile
5. Ensure thread safety and proper error handling
6. Write unit tests for the C module

### Adding Frontend Features (Node.js/React)
1. Create component under `app/dashboard/src/components/`
2. Add state management if needed (Redux/Zustand)
3. Implement API service layer for backend communication
4. Add unit tests with Jest and React Testing Library
5. Update styling with CSS modules or Tailwind

### General Guidelines
- Follow existing code style and patterns
- Write comprehensive tests for new features
- Update documentation alongside code changes
- Ensure backward compatibility
- Perform security review for new features
- Test on all supported platforms

---

🎉 **Spirit Realm is ready to protect your network with polyglot power!**

> **Effective security requires vigilance, adaptation, and the right tools for the job.**  
> Choose the right language for each task, and let your defenses evolve with the threats. 🔥
