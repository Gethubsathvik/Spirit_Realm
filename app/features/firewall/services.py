import json
from scapy.all import IP, TCP, send
from app.config import Config
from app.core.database import get_db_connection
from app.core.logger import setup_logger
from app.core.firewall_os import block_traffic_os_firewall
from app.features.firewall.engine import threat_detector
from app.features.devices.scanner import DEVICE_PROFILES, DeviceScanner
from app.features.devices.services import DeviceService

logger = setup_logger(__name__)

class FirewallService:
    @staticmethod
    def send_tcp_reset(src_ip, dst_ip, dport):
        """Sends a forged TCP RST packet to kill a connection."""
        try:
            rst_packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=8080, dport=dport, flags="R")
            send(rst_packet, verbose=0, iface=Config.INTERFACE)
            logger.warning(f"[!] TCP RST sent to {dst_ip}:{dport}")
        except Exception as e:
            logger.error(f"[-] Failed to send TCP RST: {e}")

    @staticmethod
    def get_policy_for_ip(ip, mac=None):
        """Get custom policy rules for an IP/MAC."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action, ports FROM policy_rules 
            WHERE active = 1 
            AND (ip_address = ? OR mac_address = ?)
            AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
        ''', (ip, mac or ''))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            action, ports = result['action'], result['ports']
            if action == "whitelist":
                return "whitelist", json.loads(ports) if ports else []
            elif action == "blacklist":
                return "blacklist", json.loads(ports) if ports else []
        
        return None, None

    @staticmethod
    def log_violation(ip, port, action, mac="unknown", profile="default", severity="medium"):
        """Log security violation with enhanced details."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO violations (target_ip, target_mac, unauthorized_port, action_taken, device_profile, severity) VALUES (?, ?, ?, ?, ?, ?)',
            (ip, mac, port, action, profile, severity)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def log_threat(threat_type, source_ip, target_ip, description, severity="medium"):
        """Log suspicious activity/threat."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO threats (threat_type, source_ip, target_ip, description, severity) VALUES (?, ?, ?, ?, ?)',
            (threat_type, source_ip, target_ip, description, severity)
        )
        conn.commit()
        conn.close()
        logger.warning(f"[THREAT] {threat_type}: {description}")

    @staticmethod
    def enforce_policy(ip, open_ports, mac="unknown"):
        """Checks open ports against allowed policy and takes action."""
        policy_type, policy_ports = FirewallService.get_policy_for_ip(ip, mac)
        
        if policy_type == "whitelist":
            logger.info(f"[✓] {ip} is whitelisted")
            return
        elif policy_type == "blacklist":
            logger.warning(f"[✗] {ip} is blacklisted - blocking all ports")
            for port in open_ports:
                FirewallService.log_violation(ip, port, "Blacklisted Device", mac, "default", "high")
                # Using a generic router IP as source for RST
                router_ip = Config.SUBNET.split('/')[0][:-1] + '254'
                FirewallService.send_tcp_reset(router_ip, ip, port)
                block_traffic_os_firewall(ip, port)
            return
        
        profile = DeviceScanner.identify_device_type(ip, open_ports)
        DeviceService.add_or_update_device(ip, mac, f"Device-{ip}", profile)
        
        allowed_ports = DEVICE_PROFILES[profile]["ports"]
        
        if threat_detector.detect_port_scanning(ip, open_ports):
            FirewallService.log_threat("Port Scanning", ip, "Local Network", f"Device {ip} scanning multiple ports", "high")
            logger.warning(f"[ALERT] Port scanning detected from {ip}")
        
        for port in open_ports:
            if port not in allowed_ports:
                logger.warning(f"[🚨] VIOLATION: {ip} has unauthorized port {port} open!")
                FirewallService.log_violation(ip, port, "TCP RST & Firewall Block", mac, profile, "medium")
                router_ip = Config.SUBNET.split('/')[0][:-1] + '254'
                FirewallService.send_tcp_reset(router_ip, ip, port)
                block_traffic_os_firewall(ip, port)
        
        if threat_detector.detect_ddos_pattern(ip):
            FirewallService.log_threat("DDoS Pattern", ip, "Local Network", f"Device {ip} showing DDoS-like behavior", "critical")
            logger.error(f"[CRITICAL] DDoS-like pattern detected from {ip}")
