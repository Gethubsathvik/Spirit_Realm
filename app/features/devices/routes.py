from flask import Blueprint, request, jsonify
from app.features.auth.services import AuthService
from app.features.devices.services import DeviceService

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/api/devices', methods=['GET'])
def api_get_devices():
    """API endpoint to get device list."""
    api_key = request.headers.get('X-API-Key', '')
    user_id = AuthService.verify_api_key(api_key)
    
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    devices = DeviceService.get_all_devices()
    return jsonify(devices)
