"""#Should display account attributes (Name, HU email, saved payment options [card info and billing addresses], purchases, and posting)
import tkinter as tk
from tkinter import messagebox
import requests

class AccountScreen:
    def __init__(self, root, user_id=1): # Default to 1 for testing
        self.root = root
        self.root.title("The Vault - My Account")
        self.root.geometry("400x600")
        self.user_id = user_id
        
        # UI Header
        tk.Label(root, text="Student Profile", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.profile_data = self.load_account_data()
        if self.profile_data:
            self.setup_ui()

    def load_account_data(self):
        #Fetches profile data from the backend API.
        try:
            response = requests.get(f"http://127.0.0.1:5000/api/account/{self.user_id}")
            return response.json()
        except:
            messagebox.showerror("Error", "Could not connect to server")
            return None

    def setup_ui(self):
        # User Attributes (Name & HU Email)
        info_frame = tk.LabelFrame(self.root, text="Account Info", padx=10, pady=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text=f"Username: {self.profile_data['name']}").pack(anchor="w")
        tk.Label(info_frame, text=f"Email: {self.profile_data['email']}").pack(anchor="w")

        # Payments (Requirement: Saved options)
        pay_frame = tk.LabelFrame(self.root, text="Payment Methods", padx=10, pady=10)
        pay_frame.pack(fill="x", padx=20, pady=10)
        for pay in self.profile_data['payments']:
            tk.Label(pay_frame, text=f"💳 {pay}").pack(anchor="w")

        # Postings (Requirement: User's items for sale)
        post_frame = tk.LabelFrame(self.root, text="My Postings", padx=10, pady=10)
        post_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if not self.profile_data['postings']:
            tk.Label(post_frame, text="No active listings").pack()
        else:
            for item in self.profile_data['postings']:
                tk.Label(post_frame, text=f"📦 {item['title']} - ${item['price']}").pack(anchor="w")

        # Action Buttons
        tk.Button(self.root, text="Edit Profile", bg="#004684", fg="white").pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.root.quit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountScreen(root)
    root.mainloop()"""