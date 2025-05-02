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
import shutil
import customtkinter as ctk
from customtkinter import CTkImage

ctk.set_appearance_mode("Light")  
# ctk.set_default_color_theme("blue") 

root = ctk.CTk()
# root = tk.Tk()
root.title("815 USSD Test Runner")


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

center_window(root, 1300, 600)

logo_color = "#FFA500"  # Example color (orange-yellow)

appium_process = None

# Left and Right Frames with grid layout for better control
left_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")  # Set background color to avoid gray
left_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nswe")

right_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")  
right_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nswe")

root.grid_columnconfigure(0, weight=4)  
root.grid_columnconfigure(1, weight=1) 

test_process = None

spinner_animation_running = False
spinner_frame_index = 0

def animate_spinner():
    global spinner_animation_running, spinner_frame_index

    if spinner_animation_running and spinner_frames:
        spinner_label.configure(image=spinner_frames[spinner_frame_index])
        spinner_frame_index = (spinner_frame_index + 1) % len(spinner_frames)
        spinner_label.after(50, animate_spinner)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_path = os.path.join(log_dir, f"test_log_{timestamp}.txt")

def is_appium_running(port=4723):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("localhost", port))
            return True  
        except socket.error:
            return False  
        

def start_appium_server():
    global appium_process
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


try:
    logo_img = Image.open(resource_path('logo.png'))
    logo_img = logo_img.resize((300, 130), Image.LANCZOS)
    tk_logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(left_frame, image=tk_logo, bg="#f5f5f5", borderwidth=0, highlightthickness=0)
    logo_label.pack(pady=(0, 20))
except Exception as e:
    # tk.Label(left_frame, text=f"Logo error: {e}").pack()
    ctk.CTkLabel(left_frame, text=f"Logo error: {e}").pack()

ctk.CTkLabel(
    left_frame, 
    text="Test Parameters", 
    font=("Arial", 18, "bold"), 
    anchor="center", 
    justify="center"
).pack(pady=(10, 20))


# form_frame = tk.Frame(left_frame)
form_frame = ctk.CTkFrame(left_frame, fg_color="#f5f5f5")
form_frame.pack()

bank_options = {
    "CBE": "1",
    "Awash": "2",
    "Dashen": "3",
}


fields = {}


def create_row(parent, label1, label2):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=15)

    # ctk.CTkLabel(row, text=f"{label1}:", width=120, anchor="w").grid(row=0, column=0, padx=(5,2))
    ctk.CTkLabel(row, text=f"{label1}:", width=120, anchor="w", font=("Arial", 15, "bold")).grid(row=0, column=0, padx=(5,2))
    entry1 = ctk.CTkEntry(row, font=("Arial", 15), width=200, height=38, show="*" if label1 == "PIN" else None)
    entry1.grid(row=0, column=1, padx=(2,5))
    fields[label1] = entry1

    # ctk.CTkLabel(row, text=f"{label2}:", width=120, anchor="w").grid(row=0, column=2, padx=(20,2))
    ctk.CTkLabel(row, text=f"{label2}:", width=120, anchor="w", font=("Arial", 15, "bold")).grid(row=0, column=2, padx=(20,2))
    entry2 = ctk.CTkEntry(row, font=("Arial", 15), width=200, height=38)
    entry2.grid(row=0, column=3, padx=(2,5))
    fields[label2] = entry2



create_row(form_frame, "PIN", "BOA Rec Act")
create_row(form_frame, "Amount", "ETL Phone")
create_row(form_frame, "Safaricom Phone", "Bank Account")



 
# ctk.CTkLabel(form_frame, text="Select Bank:").pack(anchor="w", pady=(10, 0))

ctk.CTkLabel(form_frame, text="Select Bank:", font=("Arial", 15, "bold")).pack(anchor="w", pady=(10, 0))

bank_var = ctk.StringVar(value="Select Bank")

bank_dropdown = ctk.CTkOptionMenu(
    form_frame,  
    variable=bank_var,
    values=list(bank_options.keys()),
    width=300,  # match other input widths
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
)

    # bank_dropdown.configure(width=450, font=("Arial", 12), bg_color=logo_color, button_color=logo_color)
    # bank_dropdown.pack(side="left", padx=5)
# bank_dropdown.pack(pady=4, ipady=6)
bank_dropdown.pack(anchor="w", pady=4, ipady=6) 



def is_valid_numeric(value):
    return value.isdigit()

def stop_test_process():
    global test_process
    if test_process and test_process.poll() is None:
        test_process.terminate()
        log_output.insert(tk.END, "\nTest process terminated by user.\n")
        write_to_logfile("Test process terminated by user.")
        test_process = None
    else:
        messagebox.showinfo("No Process", "No test is currently running.")


def run_test_in_thread():

    global test_process

    try:
       log_output.delete("1.0", tk.END)
       values = {label: entry.get().strip() for label, entry in fields.items()}

       if not bank_options[bank_var.get()]:
         messagebox.showerror("All values are required")
         return
       
       values["Bank"] = bank_options[bank_var.get()]
    #    print(values)
       script_path = resource_path("test_app.py")
    #    script_path = resource_path("test_runner.exe")

       if not os.path.exists(script_path):
         messagebox.showerror("File Error", "test_runner.exe or test_app not found.")
         return
       
       timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       separator = f"\n{'='*17}  New Test Started at {timestamp}  {'='*17}\n"
       log_output.insert(tk.END, separator)
       log_output.see(tk.END)
       write_to_logfile(separator)

       main_dir = os.path.dirname(sys.argv[0])
       
       test_process = subprocess.Popen(
           
            [sys.executable, script_path] + list(values.values()),
            # [script_path] + list(values.values()),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

       for line in test_process.stdout:
            log_output.insert(tk.END, line)
            log_output.see(tk.END)
            write_to_logfile(line.strip())


       test_process.stdout.close()
       # process.wait()
       return_code = test_process.wait()


       if return_code != 0:
            log_output.insert(tk.END, f"\n Test failed with exit code {return_code}.\n")
            write_to_logfile(f"\nTest failed with exit code {return_code}.\n")
       else:
            log_output.insert(tk.END, "\n Test completed.\n")
            write_to_logfile("\nTest completed.\n")

    except Exception as e:
        # messagebox.showerror("Input Error", "All fields are required.")
        log_output.insert(tk.END, f"\nError running test: {e}\n")
        write_to_logfile(f"\nError running test: {e}\n")
        
    finally:
        test_process = None
        log_output.see(tk.END)
        run_button.after(0, lambda: run_button.configure(state="normal", fg_color=logo_color, text_color="white"))
        spinner_label.after(0, lambda: spinner_label.pack_forget())
        spinner_label.after(0, lambda: stop_spinner())

def stop_spinner():
    global spinner_animation_running
    spinner_animation_running = False


def write_to_logfile(message):

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")


def validate_cbe(account):
    return len(account) == 13 and account.startswith("1000")

def validate_awash(account):
    return account.startswith("925")

def validate_dashen(account):
    return account.startswith("234")



run_row_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
run_row_frame.pack(pady=20)

# Spinner image (use CTkImage for CustomTkinter compatibility)
spinner_path = resource_path("spinner2.gif")


# Load spinner GIF and extract all frames
spinner_image_raw = Image.open(spinner_path)
spinner_frames = []

try:
    while True:
        frame = spinner_image_raw.copy()
        frame_ctk = CTkImage(light_image=frame, size=(30, 30))
        spinner_frames.append(frame_ctk)
        spinner_image_raw.seek(len(spinner_frames))  # go to next frame
except EOFError:
    pass 


spinner_image_raw = Image.open(spinner_path)
spinner_ctk = CTkImage(light_image=spinner_image_raw, size=(30, 30))  # adjust size if needed

spinner_label = ctk.CTkLabel(run_row_frame, text="", image=spinner_ctk)
spinner_label.pack(side="left", padx=(10, 0))
spinner_label.pack_forget()  # Hide initially

# Frame that holds both the Run Test button and the spinner
# run_row_frame = ctk.CTkFrame(left_frame)
# run_row_frame.pack(pady=10)  


def run_test():
    global test_process
    # log_output.delete("1.0", tk.END)
    # run_button.configure(state="disabled")
    # spinner_label.pack(side="left", padx=(10, 0)) 

    if test_process and test_process.poll() is None:
        messagebox.showinfo("Test Running", "A test is already running.")
        return
    
    values = {label: entry.get().strip() for label, entry in fields.items()}

    if not all(values.values()):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    for label in ["PIN", "BOA Rec Act", "ETL Phone", "Bank Account"]:
        if not is_valid_numeric(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only numbers.")
            return

    selected_bank = bank_var.get()
    bank_account = values["Bank Account"]


    if selected_bank == "Select Bank":
        messagebox.showerror("Validation Error", "Please select a Bank.")
        return
    
    elif selected_bank == "CBE" and not validate_cbe(bank_account):
        messagebox.showerror("Validation Error", "Invalid CBE Account.")
        return
    elif selected_bank == "Awash" and not validate_awash(bank_account):
        messagebox.showerror("Validation Error", "Invalid Awash Account.")
        return
    elif selected_bank == "Dashen" and not validate_dashen(bank_account):
        messagebox.showerror("Validation Error", "Invalid Dashen Account.")
        return


    if not wait_for_appium_ready():
        messagebox.showerror("Appium Error", "Appium is not ready. Please check the server.")
        return


    run_button.configure(
    state="disabled", 
    fg_color="#ffe066",     # soft yellow
    text_color="#ffffff"     # dark text while disabled (optional)
    )
    spinner_label.pack(side="left", padx=(10, 0))

    global spinner_animation_running, spinner_frame_index
    spinner_animation_running = True
    spinner_frame_index = 0
    animate_spinner()


    # threading.Thread(target=run_test_in_thread).start()

    threading.Thread(target=run_test_in_thread, daemon=True).start()

# run_button = ctk.CTkButton(left_frame, text="Run Test", font=("Arial", 15), fg_color=logo_color, hover_color="#FFA500", command=run_test)
# run_button.pack(pady=15)

run_button = ctk.CTkButton(
    run_row_frame,
    # left_frame, 
    text="Run Test", 
    font=("Arial", 14, "bold"), 
    fg_color=logo_color, 
    hover_color="#ffba00", 
    height=40,
    corner_radius=8,
    command=run_test
    # command=lambda: threading.Thread(target=run_test, daemon=True).start()
)
# run_button.pack(pady=15)
# run_button.pack(pady=15)
run_button.pack(side="left")

# btn = tb.Button(left_frame, text="Run Test", bootstyle=SUCCESS, command=run_test)
# btn.pack(pady=10)


# ctk.CTkLabel(right_frame, text="Test Logs:").pack(anchor="w")

ctk.CTkLabel(
    right_frame, 
    text="Test Log", 
    font=("Arial", 16, "bold"), 
    anchor="center", 
    justify="center"
).pack(pady=(10, 5))


log_output = ScrolledText(right_frame, height=20, font=("Courier", 8) ,wrap=tk.WORD)
log_output.pack(fill="both", expand=True)


def on_closing():
    root.destroy()
    terminate_appium() 
    os._exit(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



#pyinstaller --onefile --noconsole --add-data "test_app2.py;." --add-data "logo.png;." --add-data "USSD_Test_Script.xlsx;." --icon=logo_icon.ico --name="ussd_tester" boa_ussd_test_gui.py

# pyinstaller --onefile --noconsole --add-data "ATM_Withdrawal;ATM_Withdrawal" --add-data "Helpers;Helpers" --add-data "USSD_Test_Script.xlsx;." --name "test_runner"  test_app2.py

# pyinstaller --onefile --noconsole --add-data "USSD_Test_Script.xlsx:." --name "test_runner" test_app2.py

# pyinstaller --onefile --noconsole --add-data "test_runner.exe;." --add-data "logo.png;."  --add-data "USSD_Test_Script.xlsx;." --icon=logo_icon.ico --name="ussd815_tester" --distpath=dist_gui  --workpath=build_gui  boa_ussd_test_gui.py

# pyinstaller --onefile --noconsole --add-data "Test.xlsx;." --name hello_excel_writer --distpath=dist_test  --workpath=build_test Test.py 