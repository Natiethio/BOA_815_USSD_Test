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
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width // 4) - (width // 4))
    y = int((screen_height // 4) - (height // 4))

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.update()

center_window(root, 1350, 670)

logo_color = "#FFA500" 

appium_process = None


left_frame = ctk.CTkFrame(root, fg_color="#f5f5f5") 
left_frame.grid(row=0, column=0, padx=10, pady=27, sticky="nswe")

right_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")  
right_frame.grid(row=0, column=1, padx=10, pady=27, sticky="nswe")

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
    logo_img = logo_img.resize((300, 110), Image.LANCZOS)
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

test_options = {
    "My Accounts" : "1",
    "Transfer" : "2",
    "Transfer to Other Bank" : "3",
    "Transfer to Own" : "4",
    "Airtime" : "5",
    "Utilities" : "6",
    # "Settings" : 7,
}



fields = {}


def create_row(parent, label1, label2=None, addon_widgets=None):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=11)

    ctk.CTkLabel(row, text=f"{label1}:", width=120, anchor="w", font=("Arial", 15, "bold")).pack(side="left", padx=(5,2))
    entry1 = ctk.CTkEntry(row, font=("Arial", 15), width=200, height=35, show="*" if label1 == "PIN" else None)
    entry1.pack(side="left", padx=(2,5))
    fields[label1] = entry1

    if label2:
        ctk.CTkLabel(row, text=f"{label2}:", width=120, anchor="w", font=("Arial", 15, "bold")).pack(side="left", padx=(20,2))
        entry2 = ctk.CTkEntry(row, font=("Arial", 15), width=200, height=35)
        entry2.pack(side="left", padx=(2,5))
        fields[label2] = entry2

    if addon_widgets:
        for widget in addon_widgets:
            widget.pack(in_=row, side="left", padx=(10, 0))
            # col += 1

create_row(form_frame, "PIN", "Name")
create_row(form_frame, "BOA Rec Act", "Amount")
create_row(form_frame, "ETL Phone", "Safaricom Phone")


modular_checkbox_var = tk.BooleanVar()
modular_var = tk.StringVar(value="Select Module")


bank_row = ctk.CTkFrame(form_frame, fg_color="transparent")
bank_row.pack(fill="x", pady=11)


ctk.CTkLabel(bank_row, text="Bank Account:", width=120, anchor="w", font=("Arial", 15, "bold")).pack(side="left", padx=(5, 2))
bank_entry = ctk.CTkEntry(bank_row, font=("Arial", 15), width=200, height=35)
bank_entry.pack(side="left", padx=(2, 5))
fields["Bank Account"] = bank_entry

modular_checkbox = ctk.CTkCheckBox(
    bank_row,
    text="Modular Test:",
    variable=modular_checkbox_var,
    font=("Arial", 15, "bold"),
    onvalue=True,
    offvalue=False,
    fg_color=logo_color,
    hover_color=logo_color
)

modular_checkbox.pack(side="left", padx=(10, 0))

modular_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=modular_var,
    values=list(test_options.keys()),
    width=80,
    font=("Arial", 12),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white"
)

modular_dropdown.pack_forget() 

def toggle_modular_dropdown():
    if modular_checkbox_var.get():
        modular_dropdown.pack(side="left", pady=3, ipady=4, padx=(10, 0))
        # modular_dropdown.pack(in_=modular_checkbox.master, side="left", padx=(10, 0))
    else:
        modular_dropdown.pack_forget()
        transfer_sub_dropdown.pack_forget()
        transfer_with_otherbank_dropdown.pack_forget()
        modular_var.set("Select Module")

modular_checkbox.configure(command=toggle_modular_dropdown)
# create_row(form_frame, "Bank Account")

transfer_submodules = {
    "1: Transfer within BOA": "1",
    "2: ATM Withdrawal": "2",
    "3: Load to TeleBirr": "3",
    "4: Transfer to M-PESA": "4",
    "5: Transfer(All)": "5"
}

transfer_with_otherbank = {
    "1: Instant" : "1",
    "2: Non Instant Transfer" : "2",
    "3  Transfer to Other Bank(All)" : "3"
}


transfer_sub_var = tk.StringVar(value="Select")

transfer_sub_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=transfer_sub_var,
    values=list(transfer_submodules.keys()),
    width=80,
    font=("Arial", 13),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=lambda selected: transfer_sub_var.set(transfer_submodules[selected])
    # command=lambda selected: transfer_sub_var.set(selected)
)
transfer_sub_dropdown.pack_forget()

transfer_with_otherbank_sub_var = tk.StringVar(value="Select")

transfer_with_otherbank_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=transfer_with_otherbank_sub_var,
    values=list(transfer_with_otherbank.keys()),
    width=60,
    font=("Arial", 11),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=lambda selected: transfer_with_otherbank_sub_var.set(transfer_with_otherbank[selected])
    # command=lambda selected: transfer_sub_var.set(selected)
)
transfer_with_otherbank_dropdown.pack_forget()

def on_modular_change(*args):
    if modular_var.get() == "Transfer":
        transfer_sub_var.set("Select")
        transfer_with_otherbank_dropdown.pack_forget()
        transfer_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(10, 0))
    elif modular_var.get() == "Transfer to Other Bank":
         transfer_with_otherbank_sub_var.set("Select")
         transfer_sub_dropdown.pack_forget()
         transfer_with_otherbank_dropdown.pack(side="left", pady=3, ipady=4, padx=(10, 0))
    else:
        transfer_sub_dropdown.pack_forget()
        transfer_sub_var.set("Select")
        transfer_with_otherbank_dropdown.pack_forget()
        transfer_with_otherbank_sub_var.set("Select")


modular_var.trace_add("write", on_modular_change)


ctk.CTkLabel(form_frame, text="Select Bank:", font=("Arial", 15, "bold")).pack(anchor="w", pady=(10, 0))

bank_var = ctk.StringVar(value="Select Bank")

bank_dropdown = ctk.CTkOptionMenu(
    form_frame,  
    variable=bank_var,
    values=list(bank_options.keys()),
    width=300,  
    font=("Arial", 15, "bold"),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
)

bank_dropdown.pack(anchor="w", pady=4, ipady=6) 


def is_valid_numeric(value):
    return value.isdigit()

def is_valid_alphabet(value):
    return value.isalpha()

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
       
       values["Bank"] = bank_options[bank_var.get()]

       if not all(values.get(field) for field in ["PIN", "BOA Rec Act", "ETL Phone", "Safaricom Phone", "Amount", "Bank Account"]):
            messagebox.showerror("Input Error", "All required fields must be filled.")
            return


       if not bank_options[bank_var.get()]:
          messagebox.showerror("Validation Error", "Please select a valid bank")
          return
       
    #    print(test_options[modular_var.get()])
       selected_module = modular_var.get()
    #    selected_submodule = transfer_sub_var.get()

       if modular_checkbox_var.get():
            if selected_module == "Select Module":
                messagebox.showerror("Validation Error", "Module Name is required when Modular Test is selected.")
                return
            

            selected_code = transfer_sub_var.get()
            selected_description = transfer_submodules.get(selected_code, "")
            selected_code_transfer_other = transfer_with_otherbank_sub_var.get()


            if selected_module == "Transfer":
                    if selected_code == "Select":
                        messagebox.showerror("Validation Error", "Please select a Transfer submodule")
                        return
                    
                    values["Module Name"] = test_options[modular_var.get()]
                    
                    values["Transfer Sub Module Name"] = transfer_sub_var.get()

                    values["Transfer OB Sub Module Name"] = ""

            elif selected_module == "Transfer to Other Bank":
                    if selected_code_transfer_other == "Select":
                        messagebox.showerror("Validation Error", "Please select a Transfer to other Bank submodule")
                        return
                    
                    values["Module Name"] = test_options[modular_var.get()]

                    values["Transfer Sub Module Name"] = ""

                    values["Transfer OB Sub Module Name"] = transfer_with_otherbank_sub_var.get()

            else:
                    values["Module Name"] = test_options[modular_var.get()]

                    values["Transfer Sub Module Name"] = ""

                    values["Transfer OB Sub Module Name"] = ""



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

def validate_BOA_Account(account):
    return len(account) >= 8

def validate_cbe(account):
    return len(account) == 13 and account.startswith("1000")

def validate_awash(account):
    return account.startswith("925")

def validate_dashen(account):
    return account.startswith("234")

def validate_ETL(phone):
    return len(phone) == 10 and phone.startswith("09")

def validate_Saf(phone):
    return len(phone) == 10 and phone.startswith("07")

def validate_Pin(pin):
    return len(pin) == 4

# def validate_Modulename(module):
    

run_row_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
run_row_frame.pack(pady=20)

spinner_path = resource_path("spinner2.gif")

spinner_image_raw = Image.open(spinner_path)
spinner_frames = []

try:
    while True:
        frame = spinner_image_raw.copy()
        frame_ctk = CTkImage(light_image=frame, size=(40, 40))
        spinner_frames.append(frame_ctk)
        spinner_image_raw.seek(len(spinner_frames))  
except EOFError:
    pass 


spinner_image_raw = Image.open(spinner_path)
spinner_ctk = CTkImage(light_image=spinner_image_raw, size=(40, 40)) 

spinner_label = ctk.CTkLabel(run_row_frame, text="", image=spinner_ctk)
spinner_label.pack(side="left", padx=(10, 0))
spinner_label.pack_forget() 
 

def run_test():
    global test_process

    if test_process and test_process.poll() is None:
        messagebox.showinfo("Test Running", "A test is already running.")
        return
    
    values = {label: entry.get().strip() for label, entry in fields.items()}

    if not all(values.values()):
        messagebox.showerror("Input Error", "All fields are required.")
        return

    for label in ["PIN", "BOA Rec Act", "ETL Phone", "Safaricom Phone", "Amount", "Bank Account"]:
        if not is_valid_numeric(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only numbers")
            return
    
    
    for label in ["PIN"]:
        if not validate_Pin(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only only four characters")
            return
        
    for label in ["Name"]:
        if not is_valid_alphabet(values[label]):
            messagebox.showerror("Validation Error", f"{label} must contain only alphabetic characters")
            return
        
    for label in ["BOA Rec Act"]:
        if not validate_BOA_Account(values[label]):
            messagebox.showerror("Validation Error", "Invalid BOA Receiver Account")
            return
        
    for label in ["ETL Phone"]:
        if not validate_ETL(values[label]):
            messagebox.showerror("Validation Error", "Invalid ethio telecom number")
            return
        
    for label in ["Safaricom Phone"]:
        if not validate_Saf(values[label]):
            messagebox.showerror("Validation Error",  "Invalid safaricom number")
            return
        

    selected_bank = bank_var.get()
    bank_account = values["Bank Account"]

    selected_module = modular_var.get()

    if modular_checkbox_var.get():
        if selected_module == "Select Module":
            messagebox.showerror("Validation Error", "Module Name is required when Modular Test is selected.")
            return   
         
        selected_sub = transfer_sub_var.get()
        selected_code_transfer_other = transfer_with_otherbank_sub_var.get()

        if selected_module == "Transfer":
           
            if selected_sub == "Select":
                messagebox.showerror("Validation Error", "Please select a Transfer submodule.")
                return
            values["Module Name"] = test_options[modular_var.get()]
            
            values["Transfer Sub Module Name"] = transfer_sub_var.get()
        else:
            values["Module Name"] = test_options[modular_var.get()]


            if selected_module == "Transfer to Other Bank":
                    if selected_code_transfer_other == "Select":
                        messagebox.showerror("Validation Error", "Please select a Transfer to other Bank submodule.")
                        return
                    values["Module Name"] = test_options[modular_var.get()]
                    
                    values["Transfer OB Sub Module Name"] = transfer_with_otherbank_sub_var.get()
            else:
                    values["Module Name"] = test_options[modular_var.get()]


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
    fg_color="#ffe066",   
    text_color="#ffffff"     
    )
    spinner_label.pack(side="left", padx=(10, 0))

    global spinner_animation_running, spinner_frame_index
    spinner_animation_running = True
    spinner_frame_index = 0
    animate_spinner()


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
)
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



# pyinstaller --onefile --noconsole --add-data "test_app2.py;." --add-data "logo.png;." --add-data "USSD_Test_Script.xlsx;." --icon=logo_icon.ico --name="ussd_tester" boa_ussd_test_gui.py

# pyinstaller --onefile --noconsole --add-data "ATM_Withdrawal;ATM_Withdrawal" --add-data "Helpers;Helpers" --add-data "USSD_Test_Script.xlsx;." --name "test_runner"  test_app2.py

# pyinstaller --onefile --noconsole --add-data "USSD_Test_Script.xlsx:." --name "test_runner" test_app2.py

# pyinstaller --onefile --noconsole --add-data "test_runner.exe;." --add-data "logo.png;."  --add-data "USSD_Test_Script.xlsx;." --icon=logo_icon.ico --name="ussd815_tester" --distpath=dist_gui  --workpath=build_gui  boa_ussd_test_gui.py

# pyinstaller --onefile --noconsole --add-data "Test.xlsx;." --name hello_excel_writer --distpath=dist_test  --workpath=build_test Test.py 