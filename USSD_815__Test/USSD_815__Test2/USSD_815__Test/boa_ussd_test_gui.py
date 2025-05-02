import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import os
import threading
import signal
import sys
import socket
import time
from datetime import datetime


root = tk.Tk()
root.title("BOA USSD Test Runner")
root.geometry("900x750")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

log_file_path = "./test_log.txt"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

def is_appium_running(port=4723):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("localhost", port))
            return True  
        except socket.error:
            return False  
        

def start_appium_server():
    try:
       
        if is_appium_running():
            print("Appium is already running.")
            return  


        appium_command = ["cmd.exe", "/c", "start", "cmd.exe", "/k", "appium --allow-insecure adb_shell"]

       
        global appium_process
        # appium_process = subprocess.Popen(appium_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        appium_process = subprocess.Popen(appium_command)
        print("Appium server started successfully.")
    
    except Exception as e:
        print(f"Error starting Appium: {e}")


def terminate_appium():
    try:
        os.system("for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :4723') do taskkill /F /PID %a")
        print("Appium server (port 4723) terminated.")
    except Exception as e:
        print(f"Failed to terminate Appium: {e}")


def wait_for_appium_ready(timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_appium_running():
            print("Appium is ready and running.")
            return True
        print("Waiting for Appium to start...")
        time.sleep(4)  
    print("Appium did not start in time.")
    return False



start_appium_server()


left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=20, pady=20, fill="y")

right_frame = tk.Frame(root)
right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)


try:
    logo_img = Image.open(resource_path('logo.png'))
    logo_img = logo_img.resize((300, 90), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(left_frame, image=tk_logo)
    logo_label.pack(pady=(0, 20))
except Exception as e:
    tk.Label(left_frame, text=f"Logo error: {e}").pack()


form_frame = tk.Frame(left_frame)
form_frame.pack()

fields = {
    # "Device ID": None,
    # "Android Version": None,
    "PIN": None,
    "Receiver Account": None,
    "Amounth": None,
    "Phone Number": None,
    "Safaricom Phone": None
}

for label in fields:
    tk.Label(form_frame, text=f"{label}:").pack(anchor="w")
    entry = tk.Entry(form_frame, font=("Arial", 12), width=45)
    entry.pack(pady=4, ipady=6)  # Increase height
    fields[label] = entry


def is_valid_numeric(value):
    return value.isdigit()


def run_test_in_thread():
    try:
       log_output.delete("1.0", tk.END)
       values = {label: entry.get().strip() for label, entry in fields.items()}
       script_path = resource_path("test_app2.py")

       if not os.path.exists(script_path):
         messagebox.showerror("File Error", "test_app2.py not found.")
         return
       
       timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       separator = f"\n{'='*32}  New Test Started at {timestamp}  {'='*32}\n"
       log_output.insert(tk.END, separator)
       log_output.see(tk.END)
       write_to_logfile(separator)
    
       process = subprocess.Popen(
            [sys.executable, script_path] + list(values.values()),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

       for line in process.stdout:
            log_output.insert(tk.END, line)
            log_output.see(tk.END)
            write_to_logfile(line.strip())


       process.stdout.close()
       # process.wait()
       return_code = process.wait()


       if return_code != 0:
            log_output.insert(tk.END, f"\n Test failed with exit code {return_code}.\n")
            write_to_logfile(f"\nTest failed with exit code {return_code}.\n")
       else:
            log_output.insert(tk.END, "\n Test completed successfully.\n")
            write_to_logfile("\nTest completed successfully.\n")

    except Exception as e:
        log_output.insert(tk.END, f"\nError running test: {e}\n")
        write_to_logfile(f"\nError running test: {e}\n")
        
    finally:
        log_output.see(tk.END)


def write_to_logfile(message):

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")


def run_test():
    log_output.delete("1.0", tk.END)
    values = {label: entry.get().strip() for label, entry in fields.items()}

    if not all(values.values()):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    for label in ["PIN", "Receiver Account", "Phone Number"]:
        if not is_valid_numeric(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only numbers.")
            return

    
    if not wait_for_appium_ready():
        messagebox.showerror("Appium Error", "Appium is not ready. Please check the server.")
        return


    threading.Thread(target=run_test_in_thread).start()


tk.Button(left_frame, text="Run Test", font=("Arial", 15), command=run_test).pack(pady=10)


tk.Label(right_frame, text="Test Logs:").pack(anchor="w")
log_output = ScrolledText(right_frame, height=20, font=("Courier", 10))
log_output.pack(fill="both", expand=True)


def on_closing():
    root.destroy()
    terminate_appium() 
    os._exit(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


# pyinstaller --onefile --add-data "test_app2.py;." --add-data "logo.png;." tkintergui.py