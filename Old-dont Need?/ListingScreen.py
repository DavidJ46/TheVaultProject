"""#Should display items

#Import dependencies
  #When an item is clicked, a window for that item to be viewed should be opened
    #Window should contain item attributes (Item, Author, Date Posted, Size, Description) and a button to purchase it

import requests
import tkinter as tk # Or your preferred UI framework
from tkinter import messagebox

class ListingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("The Vault")
        self.api_url = "http://127.0.0.1:5000/api/listings/"
        
        self.label = tk.Label(root, text="Student-Owned Brands", font=("Arial", 18, "bold"))
        self.label.pack(pady=10)

        self.display_listings()

    def fetch_listings(self):
        #Calls backend API to get current listings.
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def open_item_details(self, item):
        #Requirement: Opens a window with Item, Author, Size, and Description.
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Viewing: {item['title']}")
        
        # Displaying requirements
        tk.Label(detail_window, text=f"Item: {item['title']}", font=("Arial", 14, "bold")).pack()
        tk.Label(detail_window, text=f"Brand: {item['brand']}").pack()
        tk.Label(detail_window, text=f"Price: ${item['price']}").pack()
        tk.Label(detail_window, text=f"Description: {item['description']}", wraplength=300).pack(pady=10)
        
        tk.Button(detail_window, text="Purchase Item", command=lambda: messagebox.showinfo("Order", "Order Placed!")).pack()

    def display_listings(self):
        #Requirement: Catalog of active marketplace listings[cite: 910].
        items = self.fetch_listings()
        
        for item in items:
            frame = tk.Frame(self.root, borderwidth=1, relief="solid", padx=10, pady=10)
            frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(frame, text=item['title'], font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(frame, text=f"By: {item['brand']}").pack(side="left", padx=20)
            tk.Label(frame, text=f"${item['price']}").pack(side="right")
            
            # Click to view details requirement [cite: 942]
            btn = tk.Button(frame, text="View", command=lambda i=item: self.open_item_details(i))
            btn.pack(side="right", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ListingScreen(root)
    root.mainloop()

    """
