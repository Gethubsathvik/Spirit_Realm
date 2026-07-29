import time
import threading
import logging
import os
from collections import defaultdict, deque
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.config import Config
from app.core.logger import setup_logger
from app.core.database import init_db
from app.features.auth.routes import auth_bp
from app.features.firewall.routes import firewall_bp
from app.features.devices.routes import devices_bp
from app.features.firewall.sniffer import packet_sniffer
from app.features.firewall.engine import advanced_firewall, initialize_default_rules
from app.features.devices.scanner import DeviceScanner
from app.features.firewall.services import FirewallService

logger = setup_logger(__name__)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(firewall_bp)
app.register_blueprint(devices_bp)

request_counts = defaultdict(deque)

def check_rate_limit(ip, max_requests=100, window=60):
    now = time.time()
    request_counts[ip].append(now)
    while request_counts[ip] and now - request_counts[ip][0] > window:
        request_counts[ip].popleft()
    return len(request_counts[ip]) <= max_requests

@app.before_request
def before_request():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        logger.warning(f"[!] Rate limit exceeded for {client_ip}")
        return jsonify({"error": "Rate limit exceeded"}), 429

def security_daemon():
    logger.info("[*] Starting Autonomous Security Daemon...")
    init_db()
    initialize_default_rules()
    while True:
        try:
            devices = DeviceScanner.discover_devices()
            for device in devices:
                ip = device['ip']
                mac = device['mac']
                open_ports = DeviceScanner.scan_ports(ip)
                if open_ports:
                    FirewallService.enforce_policy(ip, open_ports, mac)
            time.sleep(60)
        except Exception as e:
            logger.error(f"[-] Daemon error: {e}")
            time.sleep(60)

def start_daemon():
    daemon_thread = threading.Thread(target=security_daemon, daemon=True)
    daemon_thread.start()
    logger.info("[+] Security daemon started")

def start_sniffer():
    sniffer_thread = threading.Thread(target=packet_sniffer, daemon=True)
    sniffer_thread.start()
    logger.info("[+] Packet sniffer started")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('spirit_security.log'),
            logging.StreamHandler()
        ]
    )
    logger.info("[*] Starting Spirit Realm Security System...")
    logger.info(f"[*] Network: {Config.SUBNET}")
    logger.info(f"[*] Interface: {Config.INTERFACE}")
    logger.info(f"[*] Dashboard: http://{Config.DASHBOARD_HOST}:{Config.DASHBOARD_PORT}")
    start_daemon()
    start_sniffer()
    app.run(
        host=Config.DASHBOARD_HOST,
        port=Config.DASHBOARD_PORT,
        debug=Config.DEBUG
    )