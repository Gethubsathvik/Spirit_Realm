import sqlite3
import os
from werkzeug.security import generate_password_hash
from app.config import Config
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(Config.DATABASE_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with enhanced tables for security features."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Violations log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            target_ip TEXT,
            target_mac TEXT,
            unauthorized_port INTEGER,
            action_taken TEXT,
            severity TEXT DEFAULT 'medium',
            device_profile TEXT
        )
    ''')
    
    # Device tracking with profiles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            mac_address TEXT,
            device_name TEXT,
            profile TEXT DEFAULT 'default',
            first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
            trust_level TEXT DEFAULT 'untrusted',
            risk_score INTEGER DEFAULT 0
        )
    ''')
    
    # Threat events (suspicious activity)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            threat_type TEXT,
            source_ip TEXT,
            target_ip TEXT,
            description TEXT,
            severity TEXT,
            resolved INTEGER DEFAULT 0
        )
    ''')
    
    # User accounts for dashboard authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME,
            active INTEGER DEFAULT 1
        )
    ''')
    
    # API keys for programmatic access
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_hash TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_used DATETIME,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Audit log for all administrative actions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            action TEXT,
            details TEXT,
            ip_address TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Whitelist/Blacklist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policy_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            mac_address TEXT,
            device_name TEXT,
            rule_type TEXT,
            action TEXT,
            ports TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            active INTEGER DEFAULT 1
        )
    ''')
    
    # Firewall Rules (Advanced)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firewall_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            action TEXT,
            priority INTEGER DEFAULT 5,
            conditions TEXT,
            hits INTEGER DEFAULT 0,
            last_hit DATETIME,
            enabled INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # IP Reputation System
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_reputation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            reputation_score INTEGER DEFAULT 0,
            threat_count INTEGER DEFAULT 0,
            last_threat DATETIME,
            blocked_until DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Blocked IPs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            block_reason TEXT,
            temporary INTEGER DEFAULT 1,
            expires_at DATETIME,
            blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Bandwidth Management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bandwidth_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            bytes_per_sec INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Active Connections (Stateful Inspection)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firewall_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT,
            dest_ip TEXT,
            source_port INTEGER,
            dest_port INTEGER,
            protocol TEXT,
            state TEXT,
            packets_sent INTEGER DEFAULT 0,
            bytes_sent INTEGER DEFAULT 0,
            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_packet DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # DDoS and Attack Events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ddos_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            source_ip TEXT,
            target_ip TEXT,
            packet_count INTEGER,
            detection_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            mitigated INTEGER DEFAULT 0,
            severity TEXT
        )
    ''')
    
    # Traffic Statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traffic_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            packets_processed INTEGER,
            packets_allowed INTEGER,
            packets_blocked INTEGER,
            total_bytes_allowed INTEGER,
            total_bytes_blocked INTEGER,
            active_connections INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("[+] Database initialized successfully with advanced firewall tables")
    
    create_default_admin()

def create_default_admin():
    """Create default admin user if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_password = generate_password_hash("Spirit@2026!")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, active) VALUES (?, ?, ?, ?)",
            ("admin", admin_password, "admin", 1)
        )
        conn.commit()
        logger.warning("[!] Default admin user created. Username: admin, Password: Spirit@2026! CHANGE THIS!")
    conn.close()
