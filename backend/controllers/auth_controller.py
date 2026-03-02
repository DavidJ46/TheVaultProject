#By Ryan Grimes 2/27/2026
#Routes login

from flask import Blueprint, request, session, redirect, url_for #Flask turns scripts into web servers. 
from services.auth_services import AuthService 
from config.db import get_db_connection 

auth_bp = Blueprint('auth', __name__)
service = AuthService()

@auth_bp.route('/login', methods=['POST']) #A function for when the login button is clicked
def login():
        user = request.form['username']
        pw = request.form['password']

        conn = get_db_connection()
        success, role = service.validate_login(user, pw, conn)
        conn.close()
        
        if success:
            session['user'] = user
            session['role'] = role #Store role in the browser cookie
            return redirect(url_for('listings'))
        
        return "Invalid Credentials."

@auth_bp.route('/signup', methods=['GET', 'POST']) #A function for when the signup button is clicked
def signup():
    if request.method == 'POST': #Submits inputted credentials to database when Submit button is clicked
        user = request.form['username'] 
        pw = request.form['password']
        email = request.form['email']

        success, message = auth_system.register_user(user, pw, email)

        if success:
            return f"{message} <a href='/login'>Login here</a>" #Directs user to login screen if credentials aren't already in database
        
        return f"Signup Failed: {message} <a href='/signup'>Try again</a>"
    
    # Ensures username, email, and password are sent securely as a "POST" request to the database when submit button is pressed 
    return '''
        <form method="post"> 
            Username: <input type="text" name="username" required><br>
            Email: <input type="email" name="email" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Sign Up">
        </form>
    '''

@auth_bp.route('/listings') # If a user was not properly logged in, they don't have access to the listing screen
def listings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    message = f"<h1>Marketplace Listings</h1><p>Hello {session['user']}, welcome to the Vault!</p>"

    if session.get('role') == 'admin': 
        message += "<p style='color:red;'><strong>ADMIN ACCESS GRANTED:</strong> You can delete any listing.</p>" #Admin has slightly different view
    
    return message