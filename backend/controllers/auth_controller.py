# By Ryan Grimes - Updated 3/19/2026
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from services.auth_services import AuthService 
from config.db import get_connection

auth_bp = Blueprint('auth', __name__)
service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')

        conn = get_connection()
        if conn is None:
            return "Database connection failed. <a href='/auth/login'>Try again</a>"

        success, role = service.validate_login(user, pw, conn)
        conn.close()
        
        if success:
            session['user'] = user
            session['role'] = role
            return redirect(url_for('auth.listings'))
        
        return "Invalid Credentials. <a href='/auth/login'>Try again</a>"
    
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form.get('username') 
        pw = request.form.get('password')
        email = request.form.get('email')

        conn = get_connection()
        if conn is None:
            return "Database connection failed. <a href='/auth/signup'>Try again</a>"

        success, message = service.register_user(user, pw, email, conn)
        conn.close()

        if success:
            flash("Signup Successful! Please login with your new credentials.", "success")
            return redirect(url_for('auth.login'))
        return f"Signup Failed: {message} <a href='/auth/signup'>Try again</a>"
    
    return render_template('signup.html')

@auth_bp.route('/listings')
def listings():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('storefront.html')

@auth_bp.route('/account')
def account():
    if 'user' not in session: 
        return redirect(url_for('auth.login'))
    return render_template('account.html')
    
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    
