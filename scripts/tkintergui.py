import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import os
import threading
import signal
import sys

# Function to locate files correctly when bundled with PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Path used by PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title("BOA USSD Test Runner")
root.geometry("900x700")

# Left and Right layout
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=20, pady=20, fill="y")

right_frame = tk.Frame(root)
right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

# Load logo image
try:
    logo_img = Image.open(resource_path('logo.png'))
    logo_img = logo_img.resize((300, 180), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(left_frame, image=tk_logo)
    logo_label.pack(pady=(0, 20))
except Exception as e:
    tk.Label(left_frame, text=f"Logo error: {e}").pack()

# Input form layout
form_frame = tk.Frame(left_frame)
form_frame.pack()

fields = {
    "Device ID": None,
    "Android Version": None,
    "PIN": None,
    "Receiver Account": None,
    "Amounth": None,
    "Phone Number": None
}

for label in fields:
    tk.Label(form_frame, text=f"{label}:").pack(anchor="w")
    entry = tk.Entry(form_frame, font=("Arial", 12), width=45)
    entry.pack(pady=4, ipady=6)  # Increase height
    fields[label] = entry

# Validation for numeric fields
def is_valid_numeric(value):
    return value.isdigit()

# Run Test button action
def run_test():
    log_output.delete("1.0", tk.END)
    values = {label: entry.get().strip() for label, entry in fields.items()}

    if not all(values.values()):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    for label in ["PIN", "Receiver Account", "Phone Number", "Android Version"]:
        if not is_valid_numeric(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only numbers.")
            return

    script_path = resource_path("test_app2.py")
    if not os.path.exists(script_path):
        messagebox.showerror("File Error", "test_app2.py not found.")
        return

    def execute():
        try:
            process = subprocess.Popen(
                [sys.executable, script_path] + list(values.values()),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in iter(process.stdout.readline, ''):
                log_output.insert(tk.END, line)
                log_output.see(tk.END)
            process.stdout.close()
            process.wait()
        except Exception as e:
            log_output.insert(tk.END, f"\nError running test: {e}\n")

    threading.Thread(target=execute).start()

# Button to trigger test
tk.Button(left_frame, text="Run Test", font=("Arial", 15), command=run_test).pack(pady=10)

# Logs panel
tk.Label(right_frame, text="Test Logs:").pack(anchor="w")
log_output = ScrolledText(right_frame, height=20, font=("Courier", 10))
log_output.pack(fill="both", expand=True)

# Clean up on close
def on_closing():
    root.destroy()
    os._exit(0)  # Forcefully exit everything including watcher if any

root.protocol("WM_DELETE_WINDOW", on_closing) 
root.mainloop()
