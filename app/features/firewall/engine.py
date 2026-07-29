import time
from collections import defaultdict, deque
from datetime import datetime
from enum import Enum
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class FirewallAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    THROTTLE = "throttle"
    ISOLATE = "isolate"
    INSPECT = "inspect"

class RuleCondition(Enum):
    PORT = "port"
    PROTOCOL = "protocol"
    IP = "ip"
    MAC = "mac"
    PAYLOAD = "payload"
    PACKET_SIZE = "packet_size"
    RATE = "rate"

class FirewallRule:
    def __init__(self, rule_id, name, action, priority=5, enabled=True):
        self.rule_id = rule_id
        self.name = name
        self.action = action
        self.priority = priority
        self.enabled = enabled
        self.conditions = {}
        self.created_at = datetime.now()
        self.hits = 0
        self.last_hit = None
    
    def add_condition(self, condition_type, values):
        if isinstance(values, list):
            self.conditions[condition_type] = values
        else:
            self.conditions[condition_type] = [values]
    
    def matches(self, packet_info):
        if not self.enabled:
            return False
        
        for condition_type, values in self.conditions.items():
            if condition_type == RuleCondition.PORT:
                if packet_info.get('port') not in values:
                    return False
            elif condition_type == RuleCondition.PROTOCOL:
                if packet_info.get('protocol') not in values:
                    return False
            elif condition_type == RuleCondition.IP:
                if packet_info.get('ip') not in values:
                    return False
            elif condition_type == RuleCondition.PAYLOAD:
                payload = packet_info.get('payload', '')
                if not any(sig in payload for sig in values):
                    return False
        
        self.hits += 1
        self.last_hit = datetime.now()
        return True
    
    def to_dict(self):
        return {
            "id": self.rule_id,
            "name": self.name,
            "action": self.action.value,
            "priority": self.priority,
            "enabled": self.enabled,
            "conditions": str(self.conditions),
            "hits": self.hits,
            "created_at": self.created_at.isoformat()
        }

class AdvancedFirewall:
    def __init__(self):
        self.rules = {}
        self.connections = defaultdict(dict)
        self.blocked_ips = set()
        self.ip_reputation = defaultdict(lambda: {"score": 0, "threats": []})
        self.bandwidth_limits = {}
        self.bandwidth_usage = defaultdict(deque)
        self.next_rule_id = 1
        self.packets_processed = 0
        self.packets_blocked = 0
        self.packets_allowed = 0
        self.connection_tracking = defaultdict(dict)
        self.suspicious_patterns = defaultdict(deque)
        self.ddos_detection = defaultdict(deque)
    
    def add_rule(self, name, action, conditions, priority=5):
        rule = FirewallRule(self.next_rule_id, name, action, priority)
        for cond_type, values in conditions.items():
            rule.add_condition(cond_type, values)
        self.rules[self.next_rule_id] = rule
        self.next_rule_id += 1
        logger.info(f"[+] Firewall rule added: {name} (Priority: {priority})")
        return rule.rule_id
    
    def get_rule_action(self, packet_info):
        sorted_rules = sorted(self.rules.values(), key=lambda r: r.priority, reverse=True)
        for rule in sorted_rules:
            if rule.matches(packet_info):
                return rule.action, rule
        return None, None
    
    def update_ip_reputation(self, ip, threat_type, severity=1):
        self.ip_reputation[ip]["score"] += severity
        self.ip_reputation[ip]["threats"].append({
            "type": threat_type,
            "timestamp": datetime.now().isoformat(),
            "severity": severity
        })
        
        if self.ip_reputation[ip]["score"] > 50:
            self.block_ip_temporary(ip, 300)
    
    def block_ip_temporary(self, ip, duration=300):
        self.blocked_ips.add(ip)
        # We can't use simple threading.Timer easily in multi-process/microservice
        # A more robust solution uses background tasks or checking expiration on access
        logger.warning(f"[!] IP {ip} temporarily blocked (Reputation: {self.ip_reputation[ip]['score']})")
    
    def unblock_ip_temporary(self, ip):
        if ip in self.blocked_ips:
            self.blocked_ips.discard(ip)
            logger.info(f"[+] IP {ip} temporary block removed")
    
    def set_bandwidth_limit(self, ip, bytes_per_sec):
        self.bandwidth_limits[ip] = bytes_per_sec
    
    def check_bandwidth_limit(self, ip, packet_size):
        if ip not in self.bandwidth_limits:
            return True
        
        now = time.time()
        self.bandwidth_usage[ip].append((now, packet_size))
        
        while self.bandwidth_usage[ip] and self.bandwidth_usage[ip][0][0] < now - 1:
            self.bandwidth_usage[ip].popleft()
        
        total_bytes = sum(size for _, size in self.bandwidth_usage[ip])
        limit = self.bandwidth_limits[ip]
        
        return total_bytes <= limit
    
    def detect_syn_flood(self, source_ip, is_syn=False):
        if is_syn:
            self.ddos_detection[source_ip].append(time.time())
            
            now = time.time()
            while self.ddos_detection[source_ip] and self.ddos_detection[source_ip][0] < now - 10:
                self.ddos_detection[source_ip].popleft()
            
            if len(self.ddos_detection[source_ip]) > 100:
                logger.critical(f"[!] SYN flood detected from {source_ip}")
                self.update_ip_reputation(source_ip, "syn_flood", 15)
                return True
        
        return False
    
    def detect_port_sweep(self, source_ip, ports):
        self.suspicious_patterns[source_ip].append({
            'timestamp': time.time(),
            'ports': ports,
            'count': len(ports)
        })
        
        now = time.time()
        while self.suspicious_patterns[source_ip] and \
              self.suspicious_patterns[source_ip][0]['timestamp'] < now - 60:
            self.suspicious_patterns[source_ip].popleft()
        
        total_ports = sum(p['count'] for p in self.suspicious_patterns[source_ip])
        if total_ports > 20:
            logger.warning(f"[!] Port sweep detected from {source_ip} ({total_ports} ports)")
            self.update_ip_reputation(source_ip, "port_sweep", 8)
            return True
        
        return False
    
    def get_stats(self):
        return {
            "packets_processed": self.packets_processed,
            "packets_allowed": self.packets_allowed,
            "packets_blocked": self.packets_blocked,
            "active_connections": len(self.connection_tracking),
            "blocked_ips": len(self.blocked_ips),
            "total_rules": len(self.rules),
            "high_reputation_ips": sum(1 for ip, rep in self.ip_reputation.items() if rep["score"] > 30)
        }

class ThreatDetector:
    def __init__(self, history_size=1000):
        self.port_scan_attempts = defaultdict(deque)
        self.ddos_patterns = defaultdict(deque)
        self.history_size = history_size
    
    def detect_port_scanning(self, source_ip, ports_found):
        self.port_scan_attempts[source_ip].append({
            'timestamp': time.time(),
            'port_count': len(ports_found),
            'ports': ports_found
        })
        
        while self.port_scan_attempts[source_ip] and \
              time.time() - self.port_scan_attempts[source_ip][0]['timestamp'] > 300:
            self.port_scan_attempts[source_ip].popleft()
        
        if len(self.port_scan_attempts[source_ip]) > 0 and \
           sum(attempt['port_count'] for attempt in self.port_scan_attempts[source_ip]) > 10:
            return True
        return False
    
    def detect_ddos_pattern(self, source_ip):
        self.ddos_patterns[source_ip].append(time.time())
        
        while self.ddos_patterns[source_ip] and \
              time.time() - self.ddos_patterns[source_ip][0] > 60:
            self.ddos_patterns[source_ip].popleft()
        
        if len(self.ddos_patterns[source_ip]) > 20:
            return True
        return False

# Global instances for the Daemon service
advanced_firewall = AdvancedFirewall()
threat_detector = ThreatDetector()

def initialize_default_rules():
    """Initialize default firewall rules."""
    advanced_firewall.add_rule(
        "Allow HTTPS",
        FirewallAction.ALLOW,
        {RuleCondition.PORT: [443]},
        priority=9
    )
    advanced_firewall.add_rule(
        "Allow HTTP",
        FirewallAction.ALLOW,
        {RuleCondition.PORT: [80]},
        priority=8
    )
    advanced_firewall.add_rule(
        "Allow DNS",
        FirewallAction.ALLOW,
        {RuleCondition.PORT: [53]},
        priority=8
    )
    advanced_firewall.add_rule(
        "Throttle SSH",
        FirewallAction.THROTTLE,
        {RuleCondition.PORT: [22]},
        priority=7
    )
    logger.info("[+] Default firewall rules initialized")
