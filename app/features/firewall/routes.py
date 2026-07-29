import json
from flask import Blueprint, request, jsonify, session, render_template_string
from app.features.auth.routes import require_login
from app.features.auth.services import AuthService
from app.features.firewall.engine import advanced_firewall, FirewallAction, RuleCondition
from app.core.database import get_db_connection
from app.core.firewall_os import block_traffic_os_firewall

firewall_bp = Blueprint('firewall', __name__)

@firewall_bp.route('/')
@require_login
def dashboard():
    """Main dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM violations ORDER BY timestamp DESC LIMIT 20")
    violations = cursor.fetchall()
    
    cursor.execute("SELECT * FROM threats ORDER BY timestamp DESC LIMIT 10")
    threats = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM devices")
    device_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM threats WHERE resolved = 0")
    active_threats = cursor.fetchone()[0]
    conn.close()
    
    fw_stats = advanced_firewall.get_stats()
    blocked_ips_list = list(advanced_firewall.blocked_ips)[:10]
    
    # HTML template could be moved to templates/ but kept here for simplicity
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 Spirit Realm Security Dashboard</title>
        <style>
            body {font-family: 'Segoe UI', Arial, sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; }
            .header {display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            h1 {margin: 0; color: #ff6b6b; }
            .logout {background: #ff6b6b; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; }
            .stats {display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card {background: #161b22; border-left: 4px solid #ff6b6b; padding: 20px; border-radius: 4px; }
            .stat-value {font-size: 28px; font-weight: bold; color: #ff6b6b; }
            .stat-label {color: #8b949e; font-size: 12px; text-transform: uppercase; }
            .section {margin-bottom: 30px; }
            .section h2 {color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
            table {width: 100%; border-collapse: collapse; background: #0d1117; }
            th, td {padding: 12px; border: 1px solid #30363d; text-align: left; }
            th {background: #161b22; font-weight: 600; }
            tr:hover {background: #161b22; }
            .critical {color: #ff6b6b; font-weight: bold; }
            .high {color: #ffa500; }
            .medium {color: #ffeb3b; }
            .firewall-stats {display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 15px 0; }
            .fw-stat {background: #161b22; padding: 15px; border-radius: 4px; border-left: 3px solid #58a6ff; }
            .fw-stat-value {font-size: 24px; font-weight: bold; color: #58a6ff; }
            .fw-stat-label {color: #8b949e; font-size: 11px; text-transform: uppercase; }
            .blocked-ip {display: inline-block; background: #ff6b6b; color: white; padding: 4px 8px; margin: 2px; border-radius: 3px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔥 Spirit Realm Security Dashboard</h1>
            <a href="/logout" class="logout">Logout</a>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{device_count}</div>
                <div class="stat-label">Monitored Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(violations)}</div>
                <div class="stat-label">Recent Violations</div>
            </div>
            <div class="stat-card">
                <div class="stat-value critical">{active_threats}</div>
                <div class="stat-label">Active Threats</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{fw_stats['packets_blocked']}</div>
                <div class="stat-label">Packets Blocked</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🛡️ Advanced Firewall Status</h2>
            <div class="firewall-stats">
                <div class="fw-stat">
                    <div class="fw-stat-value">{fw_stats['packets_processed']}</div>
                    <div class="fw-stat-label">Packets Processed</div>
                </div>
                <div class="fw-stat">
                    <div class="fw-stat-value">{fw_stats['packets_allowed']}</div>
                    <div class="fw-stat-label">Packets Allowed</div>
                </div>
                <div class="fw-stat">
                    <div class="fw-stat-value critical">{fw_stats['packets_blocked']}</div>
                    <div class="fw-stat-label">Packets Blocked</div>
                </div>
                <div class="fw-stat">
                    <div class="fw-stat-value">{fw_stats['total_rules']}</div>
                    <div class="fw-stat-label">Active Rules</div>
                </div>
            </div>
            <p><strong>Connections Tracked:</strong> {fw_stats['active_connections']} | 
               <strong>Blocked IPs:</strong> {fw_stats['blocked_ips']}</p>
            <p><strong>Recently Blocked IPs:</strong></p>
            <div>{"".join(f'<span class="blocked-ip">{ip}</span>' for ip in blocked_ips_list)}</div>
        </div>
        
        <div class="section">
            <h2>Recent Security Violations</h2>
            <table>
                <tr><th>Timestamp</th><th>Device IP</th><th>MAC</th><th>Port</th><th>Action</th><th>Severity</th></tr>
                {"".join(f"<tr><td>{v['timestamp']}</td><td>{v['target_ip']}</td><td>{v['target_mac']}</td><td>{v['unauthorized_port']}</td><td>{v['action_taken']}</td><td class='{v['severity']}'>{v['severity']}</td></tr>" for v in violations)}
            </table>
        </div>
        
        <div class="section">
            <h2>Detected Threats</h2>
            <table>
                <tr><th>Timestamp</th><th>Type</th><th>Source IP</th><th>Description</th><th>Severity</th></tr>
                {"".join(f"<tr><td>{t['timestamp']}</td><td>{t['threat_type']}</td><td>{t['source_ip']}</td><td>{t['description']}</td><td class='{t['severity']}'>{t['severity']}</td></tr>" for t in threats)}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@firewall_bp.route('/api/violations', methods=['GET'])
def api_get_violations():
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    limit = min(request.args.get('limit', 50, type=int), 500)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, target_ip, target_mac, unauthorized_port, action_taken, severity 
        FROM violations ORDER BY timestamp DESC LIMIT ?
    ''', (limit,))
    violations = [{"timestamp": v['timestamp'], "ip": v['target_ip'], "mac": v['target_mac'], "port": v['unauthorized_port'], "action": v['action_taken'], "severity": v['severity']} for v in cursor.fetchall()]
    conn.close()
    
    return jsonify(violations)

@firewall_bp.route('/api/whitelist', methods=['POST'])
def api_add_whitelist():
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    ip = data.get('ip', '')
    ports = data.get('ports', [80, 443])
    
    if not ip or len(ip) > 15:
        return jsonify({"error": "Invalid IP"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO policy_rules (ip_address, action, ports, active)
        VALUES (?, ?, ?, 1)
    ''', (ip, 'whitelist', json.dumps(ports)))
    conn.commit()
    conn.close()
    
    AuthService.log_audit(user_id, "WHITELIST_ADD", f"IP {ip} whitelisted", request.remote_addr)
    return jsonify({"status": "IP whitelisted"})

@firewall_bp.route('/api/firewall/stats', methods=['GET'])
def api_firewall_stats():
    api_key = request.headers.get('X-API-Key', '')
    if not AuthService.verify_api_key(api_key): return jsonify({"error": "Unauthorized"}), 401
    return jsonify(advanced_firewall.get_stats())

@firewall_bp.route('/api/firewall/rules', methods=['GET'])
def api_get_firewall_rules():
    api_key = request.headers.get('X-API-Key', '')
    if not AuthService.verify_api_key(api_key): return jsonify({"error": "Unauthorized"}), 401
    rules = [rule.to_dict() for rule in advanced_firewall.rules.values()]
    return jsonify(rules)

@firewall_bp.route('/api/firewall/rule', methods=['POST'])
def api_add_firewall_rule():
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    if not user_id: return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    name = data.get('name', '')
    action = FirewallAction(data.get('action', 'allow'))
    ports = data.get('ports', [])
    priority = data.get('priority', 5)
    
    conditions = {RuleCondition.PORT: ports} if ports else {}
    rule_id = advanced_firewall.add_rule(name, action, conditions, priority)
    AuthService.log_audit(user_id, "FIREWALL_RULE_ADD", f"Added rule: {name}", request.remote_addr)
    return jsonify({"rule_id": rule_id, "status": "Rule added"})

@firewall_bp.route('/api/firewall/blocked-ips', methods=['GET'])
def api_get_blocked_ips():
    api_key = request.headers.get('X-API-Key', '')
    if not AuthService.verify_api_key(api_key): return jsonify({"error": "Unauthorized"}), 401
    
    blocked = list(advanced_firewall.blocked_ips)
    reputation = {ip: advanced_firewall.ip_reputation[ip] for ip in blocked}
    return jsonify({"blocked_ips": blocked, "reputation_data": reputation, "count": len(blocked)})

@firewall_bp.route('/api/firewall/block-ip', methods=['POST'])
def api_block_ip():
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    if not user_id: return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    ip = data.get('ip', '')
    duration = data.get('duration', 300)
    
    if not ip: return jsonify({"error": "Invalid IP"}), 400
    
    advanced_firewall.block_ip_temporary(ip, duration)
    block_traffic_os_firewall(ip, "1-65535")
    AuthService.log_audit(user_id, "FIREWALL_BLOCK_IP", f"Blocked IP {ip} for {duration}s", request.remote_addr)
    return jsonify({"status": f"IP {ip} blocked for {duration} seconds"})

@firewall_bp.route('/api/firewall/ip-reputation', methods=['GET'])
def api_get_ip_reputation():
    api_key = request.headers.get('X-API-Key', '')
    if not AuthService.verify_api_key(api_key): return jsonify({"error": "Unauthorized"}), 401
    
    ip = request.args.get('ip', '')
    if not ip: return jsonify({"error": "IP parameter required"}), 400
    
    rep = advanced_firewall.ip_reputation.get(ip, {"score": 0, "threats": []})
    return jsonify({"ip": ip, "reputation_score": rep["score"], "threats": rep["threats"][:10]})

@firewall_bp.route('/api/firewall/bandwidth-limit', methods=['POST'])
def api_set_bandwidth_limit():
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    if not user_id: return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    ip = data.get('ip', '')
    bytes_per_sec = data.get('bytes_per_sec', 1000000)
    
    if not ip or bytes_per_sec < 0: return jsonify({"error": "Invalid parameters"}), 400
    
    advanced_firewall.set_bandwidth_limit(ip, bytes_per_sec)
    AuthService.log_audit(user_id, "FIREWALL_BANDWIDTH", f"Set limit for {ip} to {bytes_per_sec} B/s", request.remote_addr)
    return jsonify({"status": f"Bandwidth limit set for {ip}"})

@firewall_bp.route('/api/firewall/ddos-events', methods=['GET'])
def api_get_ddos_events():
    api_key = request.headers.get('X-API-Key', '')
    if not AuthService.verify_api_key(api_key): return jsonify({"error": "Unauthorized"}), 401
    
    limit = min(request.args.get('limit', 50, type=int), 200)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT event_type, source_ip, target_ip, packet_count, detection_time, severity FROM ddos_events ORDER BY detection_time DESC LIMIT ?''', (limit,))
    events = [{"type": e['event_type'], "source_ip": e['source_ip'], "target_ip": e['target_ip'], "packet_count": e['packet_count'], "detection_time": e['detection_time'], "severity": e['severity']} for e in cursor.fetchall()]
    conn.close()
    return jsonify(events)
