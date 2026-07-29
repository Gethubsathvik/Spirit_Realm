import hashlib
import sqlite3
from werkzeug.security import check_password_hash
from app.core.database import get_db_connection
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class AuthService:
    @staticmethod
    def verify_api_key(api_key):
        """Verify API key and return user_id."""
        if not api_key:
            return None
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id FROM api_keys 
            WHERE key_hash = ? AND active = 1
        ''', (key_hash,))
        result = cursor.fetchone()
        conn.close()
        return result['user_id'] if result else None

    @staticmethod
    def authenticate_user(username, password, ip_address="127.0.0.1"):
        """Authenticate user by username and password."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ? AND active = 1", (username,))
        result = cursor.fetchone()
        
        if result and check_password_hash(result['password_hash'], password):
            user_id = result['id']
            logger.info(f"[+] User {username} logged in")
            AuthService.log_audit(user_id, "LOGIN", f"User logged in from {ip_address}", ip_address)
            conn.close()
            return user_id
            
        conn.close()
        logger.warning(f"[-] Failed login attempt for {username}")
        return None

    @staticmethod
    def log_audit(user_id, action, details, ip_address="127.0.0.1"):
        """Log administrative actions for audit trail."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO audit_log (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
            (user_id, action, details, ip_address)
        )
        conn.commit()
        conn.close()
