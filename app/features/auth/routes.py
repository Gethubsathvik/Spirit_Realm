from flask import Blueprint, request, redirect, url_for, session, jsonify
from functools import wraps
from app.features.auth.services import AuthService

auth_bp = Blueprint('auth', __name__)

def require_login(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Sanitize input
        if len(username) > 100 or len(password) > 100:
            return "Invalid credentials", 401
            
        user_id = AuthService.authenticate_user(username, password, request.remote_addr)
        
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('firewall.dashboard'))
            
        return "Invalid credentials", 401
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spirit Realm - Login</title>
        <style>
            body { background: #0d1117; color: #c9d1d9; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .login-box { background: #161b22; padding: 40px; border-radius: 8px; width: 300px; border: 1px solid #30363d; }
            h1 { color: #ff6b6b; text-align: center; }
            input { width: 100%; padding: 10px; margin: 10px 0; background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; border-radius: 4px; }
            button { width: 100%; padding: 10px; background: #ff6b6b; border: none; color: white; cursor: pointer; border-radius: 4px; font-weight: bold; }
            button:hover { background: #ff5252; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🔥 Spirit Realm Security</h1>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """

@auth_bp.route('/logout')
def logout():
    """User logout."""
    user_id = session.get('user_id')
    if user_id:
        AuthService.log_audit(user_id, "LOGOUT", "User logged out", request.remote_addr)
    session.clear()
    return redirect(url_for('auth.login'))
