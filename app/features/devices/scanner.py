import nmap
from scapy.all import ARP, Ether, srp
from app.config import Config
from app.core.logger import setup_logger

logger = setup_logger(__name__)

DEVICE_PROFILES = {
    "default": {"ports": [80, 443], "risk": "medium", "description": "Default device"},
    "router": {"ports": [80, 443, 22, 53], "risk": "high", "description": "Network Router"},
    "camera": {"ports": [80, 443, 8080], "risk": "medium", "description": "IP Camera"},
    "printer": {"ports": [80, 443, 9100], "risk": "low", "description": "Network Printer"},
    "workstation": {"ports": [80, 443, 445, 3389], "risk": "high", "description": "Windows Workstation"},
    "nas": {"ports": [80, 443, 445, 22], "risk": "high", "description": "NAS Storage"},
}

class DeviceScanner:
    @staticmethod
    def discover_devices(subnet=None):
        """Uses ARP to find active devices on the subnet."""
        subnet = subnet or Config.SUBNET
        try:
            logger.info(f"[*] Scanning subnet {subnet} for active devices...")
            arp_request = ARP(pdst=subnet)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp_request
            result = srp(packet, timeout=3, verbose=0, iface=Config.INTERFACE)[0]
            
            devices = []
            for sent, received in result:
                devices.append({'ip': received.psrc, 'mac': received.hwsrc})
            
            logger.info(f"[+] Found {len(devices)} devices on {subnet}")
            return devices
        except Exception as e:
            logger.error(f"[-] Discovery error: {e}. Check if you have root/admin privileges.")
            return []

    @staticmethod
    def scan_ports(ip):
        """Uses Nmap to scan open ports on a specific IP."""
        try:
            nm = nmap.PortScanner()
            logger.info(f"[*] Scanning ports on {ip}...")
            nm.scan(ip, '1-1024', arguments='-T4 -F')
            
            if ip in nm.all_hosts():
                open_ports = []
                for proto in nm[ip].all_protocols():
                    lport = nm[ip][proto].keys()
                    for port in lport:
                        if nm[ip][proto][port]['state'] == 'open':
                            open_ports.append(port)
                
                if open_ports:
                    logger.info(f"[+] {ip} has open ports: {open_ports}")
                
                return open_ports
        except Exception as e:
            logger.error(f"[-] Nmap error on {ip}: {e}. Make sure nmap is installed.")
        return []

    @staticmethod
    def identify_device_type(ip, open_ports):
        """Identify device type based on open ports."""
        port_set = set(open_ports)
        
        if 3389 in port_set:
            return "workstation"
        elif 9100 in port_set:
            return "printer"
        elif 445 in port_set:
            return "nas"
        elif {80, 443, 8080}.intersection(port_set):
            return "camera"
        
        return "default"
