from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from ..auth import verify_password, load_users, save_users

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        try:
            validate_csrf(request.form.get('csrf_token'))
        except ValidationError:
            flash('Invalid request. Please try again.', 'error')
            return render_template('auth/login.html')
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('auth/login.html')
        
        if verify_password(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect to next page if specified, otherwise go to main page
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@bp.route("/logout")
def logout():
    """Logout user"""
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route("/users")
def manage_users():
    """User management page (only for admin)"""
    if session.get('username') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    users = load_users()
    return render_template('auth/users.html', users=users)

@bp.route("/add-user", methods=["POST"])
def add_user():
    """Add a new user"""
    if session.get('username') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        validate_csrf(request.form.get('csrf_token'))
    except ValidationError:
        flash('Invalid request. Please try again.', 'error')
        return redirect(url_for('auth.manage_users'))
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        flash('Please enter both username and password.', 'error')
        return redirect(url_for('auth.manage_users'))
    
    users = load_users()
    if username in users:
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.manage_users'))
    
    users[username] = password
    if save_users(users):
        flash(f'User "{username}" added successfully.', 'success')
    else:
        flash('Error saving user.', 'error')
    
    return redirect(url_for('auth.manage_users'))

@bp.route("/delete-user/<username>")
def delete_user(username):
    """Delete a user"""
    if session.get('username') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    if username == 'admin':
        flash('Cannot delete admin user.', 'error')
        return redirect(url_for('auth.manage_users'))
    
    users = load_users()
    if username in users:
        del users[username]
        if save_users(users):
            flash(f'User "{username}" deleted successfully.', 'success')
        else:
            flash('Error deleting user.', 'error')
    else:
        flash('User not found.', 'error')
    
    return redirect(url_for('auth.manage_users'))
