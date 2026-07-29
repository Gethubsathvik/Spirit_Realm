import os
import platform
import secrets
import json

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    
    SUBNET = os.getenv('SUBNET', "192.168.1.0/24")
    
    @staticmethod
    def get_default_interface():
        system = platform.system()
        if system == 'Windows':
            return os.getenv('INTERFACE', 'Wi-Fi')
        elif system == 'Darwin':
            return os.getenv('INTERFACE', 'en0')
        elif system == 'Linux':
            return os.getenv('INTERFACE', 'eth0')
        else:
            return os.getenv('INTERFACE', 'eth0')
    
    INTERFACE = os.getenv('INTERFACE', None) or Config.get_default_interface()
    
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'spirit_security.db')
    
    DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', '127.0.0.1')
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_FILE = os.path.join(BASE_DIR, 'spirit_security.log')
    
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
    
    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_PATH):
            with open(cls.CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
            return cfg
        return {}
