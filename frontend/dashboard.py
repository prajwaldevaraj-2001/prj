import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://localhost:5000"

def fetch_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch inventory: {e}")
        return []

def display_inventory():
    inventory = fetch_inventory()
    for widget in frame.winfo_children():
        widget.destroy()
    for product in inventory:
        tk.Label(frame, text=f"ProductID: {product['ProductID']} | StockLevel: {product['StockLevel']}").pack()

root = tk.Tk()
root.title("Inventory Dashboard")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

btn_refresh = tk.Button(root, text="Refresh", command=display_inventory)
btn_refresh.pack()

display_inventory()
root.mainloop()
