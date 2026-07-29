import os
import subprocess
import platform
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def block_traffic_os_firewall(ip, port):
    """Uses local OS firewall to block traffic from an IP/Port."""
    try:
        system = platform.system()
        if system == 'Windows':
            rule_name = f"Fire_Block_{port}_{ip.replace('.', '_')}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=TCP remoteip={ip} remoteport={port} enable=yes'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"[🛡️] Windows Firewall rule added: {rule_name}")
        elif system == 'Darwin':
            rule = f"block drop in quick proto tcp from {ip} to any port {port}"
            cmd = f'echo "{rule}" | sudo pfctl -a com.fire.block -f - 2>/dev/null'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning(f"[⚠️] macOS pfctl failed (may need pf enabled). Trying socketfilterfw...")
                cmd2 = f'sudo socketfilterfw --add {ip} --block'
                subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.info(f"[🛡️] macOS socketfilterfw rule added for {ip}")
            else:
                logger.info(f"[🛡️] macOS pf rule added for {ip}:{port}")
        else:
            if os.path.exists('/system/bin/su') or os.path.exists('/system/xbin/su'):
                cmd = f'su -c "iptables -A INPUT -p tcp -s {ip} --dport {port} -j DROP"'
                logger.info(f"[🛡️] Android iptables rule added for {ip}:{port}")
            else:
                cmd = f'sudo iptables -A INPUT -p tcp -s {ip} --dport {port} -j DROP'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info(f"[🛡️] Linux iptables rule added for {ip}:{port}")
    except Exception as e:
        logger.error(f"[-] Failed to add firewall rule: {e}")
