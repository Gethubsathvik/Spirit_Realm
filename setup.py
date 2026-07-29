#!/usr/bin/env python3
"""
Spirit Realm - Network Security Setup Guide
Quickly configure and test your Spirit Realm installation
"""

import sqlite3
import subprocess
import sys
import os
from datetime import datetime

def check_requirements():
    """Check if all required packages are installed."""
    print("[*] Checking requirements...")
    try:
        import scapy
        import flask
        import nmap
        import flask_cors
        import werkzeug
        print("[✓] All requirements installed!")
        return True
    except ImportError as e:
        print(f"[!] Missing package: {e}")
        print("\n[*] Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        return True

def setup_database():
    """Initialize the database."""
    print("\n[*] Setting up database...")
    from app.core.database import init_db
    init_db()
    print("[✓] Database initialized!")

def generate_api_key():
    """Generate an API key for a user."""
    import hashlib
    import datetime
    
    print("\n[*] Generating API key...")
    username = input("Enter username: ").strip()
    
    conn = sqlite3.connect('spirit_security.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"[!] User '{username}' not found!")
        conn.close()
        return
    
    # Generate API key
    import secrets
    api_key = secrets.token_hex(16)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Store in database
    cursor.execute('''
        INSERT INTO api_keys (key_hash, user_id, name)
        VALUES (?, ?, ?)
    ''', (key_hash, user[0], f"Generated {datetime.now().strftime('%Y-%m-%d')}"))
    
    conn.commit()
    conn.close()
    
    print(f"\n[✓] API Key Generated!")
    print(f"Key: {api_key}")
    print("[!] Save this key securely. You won't see it again!")
    print(f"\nUsage: curl -H 'X-API-Key: {api_key}' http://127.0.0.1:5000/api/devices")

def change_admin_password():
    """Change the admin password."""
    from werkzeug.security import generate_password_hash
    
    print("\n[*] Changing admin password...")
    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    
    if new_password != confirm_password:
        print("[!] Passwords don't match!")
        return
    
    if len(new_password) < 8:
        print("[!] Password must be at least 8 characters!")
        return
    
    password_hash = generate_password_hash(new_password)
    
    conn = sqlite3.connect('security_log.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (password_hash,))
    conn.commit()
    conn.close()
    
    print("[✓] Admin password changed successfully!")

def view_violations():
    """View recent security violations."""
    print("\n[*] Recent Security Violations:")
    print("-" * 80)
    
    conn = sqlite3.connect('spirit_security.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, target_ip, target_mac, unauthorized_port, severity
        FROM violations
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    
    results = cursor.fetchall()
    if not results:
        print("[*] No violations recorded yet!")
        conn.close()
        return
    
    for violation in results:
        print(f"{violation[0]} | {violation[1]:15} | {violation[2]:17} | Port {violation[3]} | {violation[4]}")
    
    conn.close()

def view_devices():
    """View monitored devices."""
    print("\n[*] Monitored Devices:")
    print("-" * 80)
    
    conn = sqlite3.connect('spirit_security.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ip_address, mac_address, device_name, profile, trust_level
        FROM devices
        ORDER BY ip_address
    ''')
    
    results = cursor.fetchall()
    if not results:
        print("[*] No devices recorded yet!")
        conn.close()
        return
    
    for device in results:
        print(f"{device[0]:15} | {device[1]:17} | {device[2]:15} | {device[3]:10} | {device[4]}")
    
    conn.close()

def main_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print("🔥 Spirit Realm Security System - Setup & Management")
    print("="*50)
    print("\n1. Check & Install Requirements")
    print("2. Setup Database")
    print("3. Change Admin Password")
    print("4. Generate API Key")
    print("5. View Recent Violations")
    print("6. View Monitored Devices")
    print("7. Start Spirit Realm Service")
    print("8. Exit")
    print("\n" + "="*50)

if __name__ == "__main__":
    from datetime import datetime
    
    while True:
        main_menu()
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == "1":
            check_requirements()
        elif choice == "2":
            check_requirements()
            setup_database()
        elif choice == "3":
            setup_database()
            change_admin_password()
        elif choice == "4":
            setup_database()
            generate_api_key()
        elif choice == "5":
            setup_database()
            view_violations()
        elif choice == "6":
            setup_database()
            view_devices()
        elif choice == "7":
            print("\n[*] Starting Spirit Realm Security Service...")
            print("[*] Dashboard: http://127.0.0.1:5000")
            print("[!] Press Ctrl+C to stop")
            try:
                subprocess.run([sys.executable, "spirit_realm.py"], check=True)
            except KeyboardInterrupt:
                print("\n[*] Service stopped.")
        elif choice == "8":
            print("[*] Goodbye!")
            break
        else:
            print("[!] Invalid option!")
