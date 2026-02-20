from loginScreen import LoginScreen

# Initialize your class
vault = LoginScreen()

# Try to register yourself as the first user
success = vault.register_user(
    username="RyanAdmin", 
    password="SecurePassword123", 
    email="ryan@example.com"
)

if success:
    print("Go to the team and tell them the Database is officially accepting users!")