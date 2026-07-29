from app.core.database import get_db_connection
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class DeviceService:
    @staticmethod
    def get_all_devices():
        """Retrieve all tracked devices."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ip_address, mac_address, device_name, profile, trust_level, risk_score FROM devices")
        devices = [{"ip": d['ip_address'], "mac": d['mac_address'], "name": d['device_name'], 
                    "profile": d['profile'], "trust": d['trust_level'], "risk": d['risk_score']} 
                   for d in cursor.fetchall()]
        conn.close()
        return devices

    @staticmethod
    def add_or_update_device(ip, mac, device_name, profile="default", trust_level="untrusted"):
        """Add or update device in the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO devices (ip_address, mac_address, device_name, profile, trust_level, last_seen)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (ip, mac, device_name, profile, trust_level))
            conn.commit()
        except Exception as e:
            logger.error(f"[-] Error adding device {ip}: {e}")
        finally:
            conn.close()
