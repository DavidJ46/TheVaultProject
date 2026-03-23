# By Ryan Grimes - Updated 3/19/2026
from flask import Blueprint, request, session, redirect, url_for, render_template
from services.auth_services import AuthService 
from config.db import get_db_connection 

auth_bp = Blueprint('auth', __name__)
service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')

        conn = get_db_connection()
        success, role = service.validate_login(user, pw, conn)
        conn.close()
        
        if success:
            session['user'] = user
            session['role'] = role
            return redirect(url_for('storefront'))
        
        return "Invalid Credentials. <a href='/auth/login'>Try again</a>"
    
    # If GET, show the login form (Needs login.html)
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form.get('username') 
        pw = request.form.get('password')
        email = request.form.get('email')

        # Assuming register_user logic exists in your service
        success, message = service.register_user(user, pw, email)

        if success:
            return f"{message} <a href='/auth/login'>Login here</a>"
        return f"Signup Failed: {message} <a href='/auth/signup'>Try again</a>"
    
    return render_template('signup.html')

@auth_bp.route('/listings')
def listings():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    return f"<h1>Marketplace Listings</h1><p>Hello {session['user']}, welcome to the Vault!</p>"