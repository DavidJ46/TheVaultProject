
import os #Allows files to manage files, see directory paths, and read environment
import psycopg2 #Allows for Python to manage PostgreSQL databases
from flask import Flask, request, redirect, url_for, session, render_template_string #Flask turns scripts into web servers. "request" allows user input, "redirect" sends users to various pages depending on input, "url_for" provides URLs for redirected pages, "session" allows for users to not have to log in each time they are redirected, and "render_template_string" produces the layout of the webpage
from werkzeug.security import generate_password_hash, check_password_hash #Werkzeug handles requests and responses between web servers and .security is the submodule for hashing and data protection.
from dotenv import load_dotenv #Loads the keys from the hidden .env file


load_dotenv()# Load environment variables from .env

#By Ryan Grimes on 2/2/2026
class LoginScreen:
    def __init__(self): # Begins login logic to intialize connection to the AWS RDS Instance
        try:
            self.conn = psycopg2.connect( #Try to connect to the database using the keys in .env. If connection is successful, the connection is saved as variable 'self.conn'
                host=os.getenv('DB_HOST'), #The web address of the database server
                database=os.getenv('DB_NAME'), #The name of the database
                user=os.getenv('DB_USER'), #database login credentials
                password=os.getenv('DB_PASSWORD') #database login credentials
            )
            print("Login Logic: Connected to AWS RDS")
        except Exception as e:
            print(f"Login Logic: Connection Error: {e}") 

    def register_user(self, username, password, email): #Stores a user's unique ID, username, password, and email into the database
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256') #Hashes the password using the pbkdf2:sha256 algorithm
        try:
            cur = self.conn.cursor() #Creates a point for data to be entered into database
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)" #Enters data into SQL database. '%s' prevents SQLi by forcing the database to treat user input strictly as data, not as executable SQL code
            cur.execute(query, (username, hashed_pw, email)) #Inputs data at cursor point
            self.conn.commit() #Saves changes
            cur.close() #Closes cursor
            return True
        except Exception as e:
            print(f"Registration Error: {e}")
            self.conn.rollback() #If connection fails, all changes are voided to prevent saving partial data
            return False

    def validate_login(self, username, password):
        try:
            cur = self.conn.cursor() #Creates a pointer
            cur.execute("SELECT password FROM users WHERE username = %s", (username,)) #Has pointer search for occurence of entered credentials
            result = cur.fetchone() #Fetches the row of data that matches the query
            cur.close() #Closes cursor

            if result and check_password_hash(result[0], password): #If username and password hash match return true
                return True
            return False
        except Exception as e:
            print(f"Login Error: {e}")
            return False

#By Ryan Grimes on 2/2/2026
#  FLASK WEB SERVER SETUP 
app = Flask(__name__) #Create website object
app.secret_key = os.urandom(24) # Encrypts session connection
auth_system = LoginScreen() #Allows the website to use functions in LoginScreen class

#By Ryan Grimes on 2/2/2026
@app.route('/') #Tells Flask to automatically run the following function when they visit the main homepage
def home():
    if 'user' in session: #Checks if user is already logged in
        return f"Logged in as {session['user']} | <a href='/logout'>Logout</a>" #Welcome screen with logout screen
    return "Welcome to The Vault! Please <a href='/login'>Login</a> or <a href='/signup'>Signup</a>." #Default screen with Login and Signup buttons

#By Ryan Grimes on 2/2/2026
@app.route('/signup', methods=['GET', 'POST']) #A function for when the signup button is clicked
def signup():
    if request.method == 'POST': #Submits inputted credentials to database when Submit button is clicked
        user = request.form['username'] 
        pw = request.form['password']
        email = request.form['email']
        if auth_system.register_user(user, pw, email):
            return "Signup Successful! <a href='/login'>Login here</a>" #Directs user to login screen if credentials aren't already in database
        return "Signup Failed (User may already exist)."
    
    # Ensures username, email, and password are sent securely as a "POST" request to the database when submit button is pressed 
    return '''
        <form method="post"> 
            Username: <input type="text" name="username"><br>
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Sign Up">
        </form>
    '''

#By Ryan Grimes on 2/2/2026
@app.route('/login', methods=['GET', 'POST']) #A function for when the login button is clicked
def login():
    if request.method == 'POST': #Requests inputted username and password from database when Login button is clicked
        user = request.form['username']
        pw = request.form['password']
        if auth_system.validate_login(user, pw): #If validate_login function returns true, the return value is stored in a browser cookie so they don't have to sign in multiple times
            session['user'] = user #Saves user credentials in browser cookie
            return redirect(url_for('listings')) #Once logged in, go to the listingScreen
        return "Invalid Credentials."

    # Ensures username and password are sent securely as a "POST" request to the database when submit button is pressed
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

#By Ryan Grimes on 2/2/2026
@app.route('/listings') # If a user was not properly logged in, they don't have access to the listing screen
def listings():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"<h1>Marketplace Listings</h1><p>Hello {session['user']}, welcome to the Vault!</p>"

#By Ryan Grimes on 2/2/2026
@app.route('/logout') #Erases the cookie allowing them access to validated screens and redirects them to login screen
def logout():
    session.pop('user', None) #Kills the session that allows access to validated screens
    return redirect(url_for('home')) #Redirects logged out user to home screen

#By Ryan Grimes on 2/2/2026
if __name__ == "__main__": #Starts webpage
    app.run(debug=True, port=5000) #Flask engine listens on localhost: 5000 for visitors and provides error messages