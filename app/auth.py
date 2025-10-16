import os
import hashlib
from functools import wraps
from flask import session, redirect, url_for, request, flash, render_template

def load_users():
    """Load users from users.txt file"""
    users = {}
    if os.path.exists('users.txt'):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        username, password = line.split(':', 1)
                        users[username] = password
        except Exception as e:
            print(f"Error loading users: {e}")
    return users

def save_users(users):
    """Save users to users.txt file"""
    try:
        with open('users.txt', 'w') as f:
            for username, password in users.items():
                f.write(f"{username}:{password}\n")
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def hash_password(password):
    """Simple password hashing (for basic security)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username, password):
    """Verify user credentials"""
    users = load_users()
    if username in users:
        # For now, storing plain text passwords (you can enhance this later)
        return users[username] == password
    return False

def create_default_user_if_not_exists():
    """Create default admin user if users.txt doesn't exist"""
    if not os.path.exists('users.txt'):
        users = {'admin': 'admin123'}
        save_users(users)
        print("[INFO] Default user created: admin/admin123")

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    """Check if user is logged in"""
    return session.get('logged_in', False)

def get_current_user():
    """Get current logged in user"""
    if session.get('logged_in'):
        return session.get('username', 'Unknown')
    return None
