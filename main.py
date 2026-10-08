import socket
import re
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk

# ----------------- سائبر سیکیورٹی پورٹ اسکینر کا حصہ -----------------
PORT_INFO = {
    21: "FTP (File Transfer) - Vulnerable to brute force if left open!",
    22: "SSH (Secure Shell) - Secure, but check for unauthorized access.",
    80: "HTTP (Web Server) - Unencrypted traffic! Use HTTPS (443) instead.",
    443: "HTTPS (Secure Web) - Secure encrypted web traffic."
}

def scan_ports():
    target = entry_target.get().strip()
    if not target:
        messagebox.showerror("Error", "Please enter an IP or Domain name!")
        return
    
    for item in tree.get_children():
        tree.delete(item)
        
    btn_scan.config(state=tk.DISABLED, text="Scanning...")
    root.update()

    for port in PORT_INFO.keys():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target, port))
        
        if result == 0:
            status = "OPEN 🔴 (Danger)"
            info = PORT_INFO[port]
        else:
            status = "CLOSED 🟢 (Safe)"
            info = "No immediate threat."
            
        tree.insert("", tk.END, values=(port, status, info))
        s.close()
        root.update()
        
    btn_scan.config(state=tk.NORMAL, text="Start Security Scan")

# ----------------- پاس ورڈ چیکر کا نیا فیچر -----------------
def check_password_strength():
    password = entry_password.get()
    if not password:
        lbl_result.config(text="Status: Please enter a password!", fg="orange")
        return
    
    # طاقت کی جانچ پڑتال کے اصول
    score = 0
    feedback = []
    
    if len(password) >= 8: score += 1
    else: feedback.append("Min 8 chars")
        
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("No Uppercase")
        
    if re.search(r"[a-z]", password): score += 1
    else: feedback.append("No Lowercase")
        
    if re.search(r"\d", password): score += 1
    else: feedback.append("No Number")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    else: feedback.append("No Special Char")
    
    # رزلٹ دکھانا
    if score <= 2:
        lbl_result.config(text="Strength: VERY WEAK 🔴 (Easy to Hack)", fg="#ff4d4d")
    elif score <= 4:
        lbl_result.config(text="Strength: MEDIUM 🟡 (Moderate Risk)", fg="#ffcc00")
    else:
        lbl_result.config(text="Strength: STRONG 🟢 (Highly Secure)", fg="#33cc33")
        
    if feedback:
        lbl_tips.config(text="Tips to improve: " + ", ".join(feedback))
    else:
        lbl_tips.config(text="Excellent! Your password is safe.")

def generate_strong_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    strong_pwd = "".join(random.choice(chars) for _ in range(12))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, strong_pwd)
    check_password_strength()

# ----------------- مین انٹرفیس (GUI) سیٹ اپ -----------------
root = tk.Tk()
root.title("Advanced Cybersecurity Tool By Saqib")
root.geometry("700x550")
root.configure(bg="#1e1e1e")

# ٹیبز (Tabs) بنانے کا عمل
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill=tk.BOTH, expand=True)

# اسٹائلنگ
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#1e1e1e")
style.configure("TNotebook.Tab", background="#2d2d2d", foreground="white", padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#007acc")])
style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d", rowheight=25)

# ----------------- ٹیب 1: پورٹ اسکینر -----------------
tab1 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab1, text=" Network Port Scanner ")

lbl_title = tk.Label(tab1, text="Basic Network Scanner", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e")
lbl_title.pack(pady=10)

frame_input = tk.Frame(tab1, bg="#1e1e1e")
frame_input.pack(pady=10)

lbl_target = tk.Label(frame_input, text="Enter Target IP / Website:", fg="white", bg="#1e1e1e", font=("Arial", 10))
lbl_target.pack(side=tk.LEFT, padx=5)

entry_target = tk.Entry(frame_input, font=("Arial", 10), width=25)
entry_target.insert(0, "amazon.com")
entry_target.pack(side=tk.LEFT, padx=5)

btn_scan = tk.Button(frame_input, text="Start Security Scan", command=scan_ports, bg="#007acc", fg="white", font=("Arial", 10, "bold"), padx=10)
btn_scan.pack(side=tk.LEFT, padx=5)

columns = ("Port", "Status", "Security Info")
tree = ttk.Treeview(tab1, columns=columns, show="headings")
tree.heading("Port", text="Port")
tree.heading("Status", text="Status")
tree.heading("Security Info", text="Security Warning / Information")
tree.column("Port", width=60, anchor=tk.CENTER)
tree.column("Status", width=120, anchor=tk.CENTER)
tree.column("Security Info", width=400, anchor=tk.W)
tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# ----------------- ٹیب 2: پاس ورڈ چیکر -----------------
tab2 = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab2, text=" Password Strength Checker ")

lbl_title2 = tk.Label(tab2, text="AI Password Security Analyzer", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e")
lbl_title2.pack(pady=20)

frame_pwd_input = tk.Frame(tab2, bg="#1e1e1e")
frame_pwd_input.pack(pady=10)

lbl_pwd = tk.Label(frame_pwd_input, text="Enter Password to Test:", fg="white", bg="#1e1e1e", font=("Arial", 11))
lbl_pwd.pack(side=tk.LEFT, padx=5)

entry_password = tk.Entry(frame_pwd_input, font=("Arial", 11), width=30, show="*")
entry_password.pack(side=tk.LEFT, padx=5)

# پاس ورڈ ٹائپ کرتے ہی چیک کرنے کے لیے
entry_password.bind("<KeyRelease>", lambda event: check_password_strength())

btn_gen = tk.Button(tab2, text="Generate Strong Password 🔑", command=generate_strong_password, bg="#28a745", fg="white", font=("Arial", 10, "bold"), pady=5)
btn_gen.pack(pady=10)

lbl_result = tk.Label(tab2, text="Strength: Waiting for input...", font=("Arial", 12, "bold"), fg="white", bg="#1e1e1e")
lbl_result.pack(pady=15)

lbl_tips = tk.Label(tab2, text="", font=("Arial", 10, "italic"), fg="#aaaaaa", bg="#1e1e1e", wraplength=500)
lbl_tips.pack(pady=10)

root.mainloop()