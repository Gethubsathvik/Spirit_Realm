from scapy.all import sniff, IP, TCP, UDP, Raw
from app.config import Config
from app.core.logger import setup_logger
from app.core.firewall_os import block_traffic_os_firewall
from app.features.firewall.engine import advanced_firewall, FirewallAction

logger = setup_logger(__name__)

def inspect_packet(packet):
    """Advanced Deep Packet Inspection."""
    try:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            ttl = packet[IP].ttl
            packet_len = len(packet)
            
            # Check for IP spoofing (TTL too high/low)
            if ttl < 10 or ttl > 255:
                advanced_firewall.update_ip_reputation(src_ip, "suspicious_ttl", 2)
            
            # Check for unusual packet size
            if packet_len > 65535:
                advanced_firewall.update_ip_reputation(src_ip, "oversized_packet", 2)
            
            # TCP Analysis
            if TCP in packet:
                sport = packet[TCP].sport
                dport = packet[TCP].dport
                flags = packet[TCP].flags
                
                # SYN flood detection
                if flags == "S":  # SYN flag
                    if advanced_firewall.detect_syn_flood(src_ip, is_syn=True):
                        block_traffic_os_firewall(src_ip, dport)
                        return "BLOCK_SYNFLOOD"
                
                # Detect port sweeping
                if dport > 1024:
                    if advanced_firewall.detect_port_sweep(src_ip, [dport]):
                        return "BLOCK_PORTSWEEP"
            
            # UDP Analysis
            if UDP in packet:
                sport = packet[UDP].sport
                dport = packet[UDP].dport
                
                # DNS Amplification Attack Detection
                if dport == 53:
                    if packet[UDP].len > 512:
                        advanced_firewall.update_ip_reputation(src_ip, "dns_amplification", 5)
            
            # Payload inspection for malware signatures
            if Raw in packet:
                payload = bytes(packet[Raw].load)
                
                # Check for known malware patterns
                malware_signatures = [
                    b"..\\..\\",  # Directory traversal
                    b"<script",   # XSS attempts
                    b"union select",  # SQL injection
                    b"exec(",    # Code execution
                ]
                
                for signature in malware_signatures:
                    if signature in payload:
                        logger.critical(f"[!] Malware signature detected in packet from {src_ip}")
                        advanced_firewall.update_ip_reputation(src_ip, "malware_signature", 10)
                        return "BLOCK_MALWARE"
            
            # Check firewall rules
            packet_info = {
                "ip": src_ip,
                "port": packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else 0),
                "protocol": "TCP" if TCP in packet else ("UDP" if UDP in packet else "ICMP"),
                "payload": str(packet)[:100]
            }
            
            action, rule = advanced_firewall.get_rule_action(packet_info)
            
            if action:
                if action == FirewallAction.ALLOW:
                    advanced_firewall.packets_allowed += 1
                    return "ALLOW"
                elif action == FirewallAction.DENY:
                    advanced_firewall.packets_blocked += 1
                    logger.warning(f"[!] Packet blocked by rule: {rule.name}")
                    return "DENY"
                elif action == FirewallAction.THROTTLE:
                    if not advanced_firewall.check_bandwidth_limit(src_ip, packet_len):
                        advanced_firewall.packets_blocked += 1
                        return "THROTTLE"
                elif action == FirewallAction.INSPECT:
                    return "INSPECT"
            
            advanced_firewall.packets_processed += 1
            advanced_firewall.packets_allowed += 1
            return "ALLOW"
    
    except Exception as e:
        logger.debug(f"[-] Packet inspection error: {e}")
    
    return "ALLOW"

def packet_sniffer():
    """Sniff packets for real-time threat detection."""
    logger.info("[*] Starting packet sniffer for advanced protection...")
    try:
        iface = Config.INTERFACE
        logger.info(f"[*] Sniffing on interface: {iface}")
        sniff(iface=iface, prn=inspect_packet, store=False, timeout=3600)
    except PermissionError:
        logger.error("[-] Packet sniffer requires root/admin privileges. Run with sudo or as Administrator.")
    except OSError as e:
        logger.error(f"[-] Interface error: {e}. Check that the interface name is correct.")
        logger.error(f"[-] Available interfaces: {get_available_interfaces()}")
    except Exception as e:
        logger.error(f"[-] Packet sniffer error: {e}. Check if you have root/admin privileges.")

def get_available_interfaces():
    """List available network interfaces."""
    try:
        from scapy.all import get_if_list
        return get_if_list()
    except Exception:
        return []
