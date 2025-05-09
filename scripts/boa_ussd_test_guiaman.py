import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import os
import threading
import socket
import time
from datetime import datetime
import customtkinter as ctk
import sys

ctk.set_appearance_mode("Light")
# ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("815 USSD Test Runner")


def center_window(root, width, height):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width // 2) - (width // 2))
    y = int((screen_height // 2) - (height // 2))

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.update()

center_window(root, 1320, 650)

logo_color = "#FFA500"

appium_process = None


left_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")
left_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nswe")  # Added padding to left_frame
left_frame.grid_columnconfigure(0, weight=1) # Make the left frame resizable

right_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")
right_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nswe") # Added padding to right frame
right_frame.grid_columnconfigure(0, weight=1) # Make the right frame resizable

root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1) # Make the row resizable




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
    logo_label.pack(pady=(0, 20), anchor="center") # Center the logo
except Exception as e:
    # tk.Label(left_frame, text=f"Logo error: {e}").pack()
    ctk.CTkLabel(left_frame, text=f"Logo error: {e}").pack()

ctk.CTkLabel(
    left_frame,
    text="Test Parameters",
    font=("Arial", 18, "bold"),
    anchor="center",
    justify="center"
).pack(pady=(10, 20), fill="x") # Use fill="x" to center the label


form_frame = ctk.CTkFrame(left_frame, fg_color="#f5f5f5")
form_frame.pack(fill="x") # Make the form frame fill the left frame

bank_options = {
    "CBE": "1",
    "Awash": "2",
    "Dashen": "3",
}

test_options = {
    "My Accounts": "1",
    "Transfer": "2",
    "Transfer to Other Bank": "3",
    "Transfer to Own": "4",
    "Airtime": "5",
    "Utilities": "6",
    # "Settings" : 7,
}

# Dictionary to hold input field widgets
input_fields = {}
fields = {}

bank_var = tk.StringVar(value="Select Bank")

def create_input_field(parent, label, is_password=False):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(5,5)) # Reduced padding
    ctk.CTkLabel(row, text=f"{label}:", width=150, anchor="w", font=("Arial", 15, "bold")).pack(side="left", padx=(5, 2))
    entry = ctk.CTkEntry(row, font=("Arial", 15), width=250, height=35, show="*" if is_password else None)
    entry.pack(side="left", padx=(2, 5), fill="x") # Make entry fill available space
    row.pack_configure(anchor="w")
    input_fields[label] = entry
    return row

# Create all possible input fields initially and pack them
pin_row = create_input_field(form_frame, "PIN", is_password=True)
boa_rec_act_row = create_input_field(form_frame, "BOA Rec Act")
amount_row = create_input_field(form_frame, "Amount")
etl_phone_row = create_input_field(form_frame, "ETL Phone")
safaricom_phone_row = create_input_field(form_frame, "Safaricom Phone")
bank_account_row = create_input_field(form_frame, "Bank Account")
name_row = create_input_field(form_frame, "Name")

# Store the entry widgets in the 'fields' dictionary for easy access later
fields["PIN"] = input_fields["PIN"].winfo_children()[1]
fields["BOA Rec Act"] = input_fields["BOA Rec Act"].winfo_children()[1]
fields["Amount"] = input_fields["Amount"].winfo_children()[1]
fields["ETL Phone"] = input_fields["ETL Phone"].winfo_children()[1]
fields["Safaricom Phone"] = input_fields["Safaricom Phone"].winfo_children()[1]
fields["Bank Account"] = input_fields["Bank Account"].winfo_children()[1]
fields["Name"] = input_fields["Name"].winfo_children()[1]


modular_checkbox_var = tk.BooleanVar()
modular_var = tk.StringVar(value="Select Module")

bank_row = ctk.CTkFrame(form_frame, fg_color="transparent")
bank_row.pack(fill="x", pady=(5,5)) 

bank_label = ctk.CTkLabel(bank_row, text="Bank:", width=120, anchor="w", font=("Arial", 15, "bold"))
bank_label.pack(side="left", padx=(5, 2))
bank_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=bank_var,
    values=list(bank_options.keys()),
    width=200,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white"
)
bank_dropdown.pack(side="left", padx=(2, 5), fill="x") # Make dropdown fill space

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
bank_row.pack_configure(anchor="w")


modular_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=modular_var,
    values=list(test_options.keys()),
    width=180,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white"
)

modular_dropdown.pack_forget()

transfer_submodules = {
    "Transfer Within BOA": "Transfer Within BOA",
    "ATM Withdrawal": "ATM Withdrawal",
    "Load to TeleBirr": "Load to TeleBirr",
    "Transfer to M-PESA": "Transfer to M-PESA",
    "Transfer(All)": "Transfer(All)"
}

transfer_with_otherbank = {
    "Instant": "Instant",
    "Non Instant Transfer": "Non Instant Transfer"
}

transfer_sub_var = tk.StringVar(value="Select")

transfer_sub_dropdown = ctk.CTkOptionMenu(
    bank_row,
    variable=transfer_sub_var,
    values=list(transfer_submodules.keys()),
    width=180,
    font=("Arial", 13),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=transfer_sub_var.set
)
transfer_sub_dropdown.pack_forget()

def update_input_fields():
    # Hide all fields first
    for row in [pin_row, boa_rec_act_row, amount_row, etl_phone_row, safaricom_phone_row, bank_account_row, name_row]:
        row.pack_forget()

    # Hide the bank dropdown and label by default
    bank_label.pack_forget()
    bank_dropdown.pack_forget()

    if not modular_checkbox_var.get():
        # Display all fields by default
        pin_row.pack(fill="x", pady=(5,5))
        boa_rec_act_row.pack(fill="x", pady=(5,5))
        amount_row.pack(fill="x", pady=(5,5))
        etl_phone_row.pack(fill="x", pady=(5,5))
        safaricom_phone_row.pack(fill="x", pady=(5,5))
        bank_account_row.pack(fill="x", pady=(5,5))
        name_row.pack(fill="x", pady=(5,5))
        # Show the bank label and dropdown
        bank_label.pack(side="left", padx=(5, 2))
        bank_dropdown.pack(side="left", padx=(2, 5), fill="x")
        bank_var.set("Select Bank")
    else:
        selected_module = modular_var.get()
        if selected_module == "My Accounts":
            pin_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Transfer":
            pin_row.pack(fill="x", pady=(5,5))
            selected_submodule_text = transfer_sub_var.get()
            if selected_submodule_text == "Transfer Within BOA":
                boa_rec_act_row.pack(fill="x", pady=(5,5))
                amount_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "ATM Withdrawal":
                pass  # Only PIN is needed
            elif selected_submodule_text == "Load to TeleBirr":
                amount_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "Transfer to M-PESA":
                amount_row.pack(fill="x", pady=(5,5))
                etl_phone_row.pack(fill="x", pady=(5,5))
                safaricom_phone_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "Transfer(All)":
                boa_rec_act_row.pack(fill="x", pady=(5,5))
                amount_row.pack(fill="x", pady=(5,5))
                etl_phone_row.pack(fill="x", pady=(5,5))
                safaricom_phone_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Transfer to Other Bank":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
            bank_account_row.pack(fill="x", pady=(5,5))
            name_row.pack(fill="x", pady=(5,5))
            # Show the bank label and dropdown only for "Transfer to Other Bank"
            bank_label.pack(side="left", padx=(5, 2))
            bank_dropdown.pack(side="left", padx=(2, 5), fill="x")
        elif selected_module == "Transfer to Own":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Airtime":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
            etl_phone_row.pack(fill="x", pady=(5,5))
            safaricom_phone_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Utilities":
            pin_row.pack(fill="x", pady=(5,5))
            boa_rec_act_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
            etl_phone_row.pack(fill="x", pady=(5,5))
            safaricom_phone_row.pack(fill="x", pady=(5,5))

    # Always pack bank_row at the end so it stays at the bottom
    bank_row.pack_forget()
    bank_row.pack(fill="x", pady=(5,5), anchor="w")

def toggle_modular_dropdown():
    if modular_checkbox_var.get():
        modular_dropdown.pack(side="left", pady=3, ipady=4, padx=(10, 0), fill="x")
        if modular_var.get() == "Transfer":
            transfer_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 0), fill="x")
        else:
            transfer_sub_dropdown.pack_forget()
    else:
        modular_dropdown.pack_forget()
        transfer_sub_dropdown.pack_forget()
        modular_var.set("Select Module")
        transfer_sub_var.set("Select")
    update_input_fields()

modular_checkbox.configure(command=toggle_modular_dropdown)

def on_modular_change(*args):
    if modular_var.get() == "Transfer":
        transfer_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 0), fill="x")
    else:
        transfer_sub_dropdown.pack_forget()
        transfer_sub_var.set("Select")
    update_input_fields()

modular_var.trace_add("write", on_modular_change)
transfer_sub_var.trace_add("write", lambda *args: update_input_fields())
modular_checkbox_var.trace_add("write", lambda *args: update_input_fields())

def is_valid_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_field_values():

    values = {}
    for field_name in ["PIN", "BOA Rec Act", "Amount", "ETL Phone", "Safaricom Phone", "Bank Account", "Name"]:
        try:
            # Try to get the value.  If the widget doesn't exist, we assume
            # the field is not relevant to the current test and use a default.
            values[field_name] = fields[field_name].get()
        except KeyError:
            values[field_name] = ""  # Or some other default value
    return values

def run_test():
    print("Run Test button pressed")  # Debug print
    bank = bank_var.get()

    if modular_checkbox_var.get():
        selected_module = modular_var.get()
        if selected_module == "Transfer to Other Bank":
            if bank == "Select Bank":
                messagebox.showerror("Error", "Please select a bank.")
                return
    else:
        # If not modular, require bank selection (if that's your intended logic)
        if bank == "Select Bank":
            messagebox.showerror("Error", "Please select a bank.")
            return

    field_values = get_field_values()
    pin = field_values["PIN"]
    boa_rec_act = field_values["BOA Rec Act"]
    amount = field_values["Amount"]
    etl_phone = field_values["ETL Phone"]
    safaricom_phone = field_values["Safaricom Phone"]
    bank_account = field_values["Bank Account"]
    name = field_values["Name"]

    if not modular_checkbox_var.get():
        if not pin:
            messagebox.showerror("Error", "PIN is required.")
            return
        if not boa_rec_act:
            messagebox.showerror("Error", "BOA Rec Act is required.")
            return
        if not amount:
            messagebox.showerror("Error", "Amount is required.")
            return
        if not is_valid_numeric(amount):
            messagebox.showerror("Error", "Amount must be a valid number.")
            return

    if modular_checkbox_var.get():
        selected_module = modular_var.get()
        if selected_module == "Select Module":
            messagebox.showerror("Error", "Please select a module.")
            return

        if selected_module == "My Accounts":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
        elif selected_module == "Transfer":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
            selected_submodule = transfer_sub_var.get()
            if selected_submodule == "Select":
                messagebox.showerror("Error", "Please select a transfer submodule.")
                return
            if selected_submodule == "Transfer Within BOA":
                if not boa_rec_act:
                    messagebox.showerror("Error", "BOA Rec Act is required.")
                    return
                if not amount:
                    messagebox.showerror("Error", "Amount is required.")
                    return
                if not is_valid_numeric(amount):
                    messagebox.showerror("Error", "Amount must be a valid number.")
                    return
            elif selected_submodule == "Load to TeleBirr":
                if not amount:
                    messagebox.showerror("Error", "Amount is required.")
                    return
                if not is_valid_numeric(amount):
                    messagebox.showerror("Error", "Amount must be a valid number.")
                    return
            elif selected_submodule == "Transfer to M-PESA":
                if not amount:
                    messagebox.showerror("Error", "Amount is required.")
                    return
                if not is_valid_numeric(amount):
                    messagebox.showerror("Error", "Amount must be a valid number.")
                    return
                if not etl_phone:
                    messagebox.showerror("Error", "ETL Phone is required.")
                    return
                if not safaricom_phone:
                    messagebox.showerror("Error", "Safaricom Phone is required.")
                    return
            elif selected_submodule == "Transfer(All)":
                if not boa_rec_act:
                    messagebox.showerror("Error", "BOA Rec Act is required.")
                    return
                if not amount:
                    messagebox.showerror("Error", "Amount is required.")
                    return
                if not is_valid_numeric(amount):
                    messagebox.showerror("Error", "Amount must be a valid number.")
                    return
                if not etl_phone:
                    messagebox.showerror("Error", "ETL Phone is required.")
                    return
                if not safaricom_phone:
                    messagebox.showerror("Error", "Safaricom Phone is required.")
                    return
        elif selected_module == "Transfer to Other Bank":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
            if not amount:
                messagebox.showerror("Error", "Amount is required.")
                return
            if not is_valid_numeric(amount):
                messagebox.showerror("Error", "Amount must be a valid number.")
                return
            if not bank_account:
                messagebox.showerror("Error", "Bank Account is required.")
                return
            if not name:
                messagebox.showerror("Error", "Name is required.")
                return
        elif selected_module == "Transfer to Own":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
            if not amount:
                messagebox.showerror("Error", "Amount is required.")
                return
            if not is_valid_numeric(amount):
                messagebox.showerror("Error", "Amount must be a valid number.")
                return
        elif selected_module == "Airtime":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
            if not amount:
                messagebox.showerror("Error", "Amount is required.")
                return
            if not is_valid_numeric(amount):
                messagebox.showerror("Error", "Amount must be a valid number.")
                return
            if not etl_phone:
                messagebox.showerror("Error", "ETL Phone is required.")
                return
            if not safaricom_phone:
                messagebox.showerror("Error", "Safaricom Phone is required.")
                return
        elif selected_module == "Utilities":
            if not pin:
                messagebox.showerror("Error", "PIN is required.")
                return
            if not boa_rec_act:
                messagebox.showerror("Error", "BOA Rec Act is required.")
                return
            if not amount:
                messagebox.showerror("Error", "Amount is required.")
                return
            if not is_valid_numeric(amount):
                messagebox.showerror("Error", "Amount must be a valid number.")
                return
            if not etl_phone:
                messagebox.showerror("Error", "ETL Phone is required.")
                return
            if not safaricom_phone:
                messagebox.showerror("Error", "Safaricom Phone is required.")
                return

    log_text.config(state=tk.NORMAL)
    log_text.delete("1.0", tk.END)
    # log_text.insert(tk.END, "Running test...\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

    run_button.configure(
    state="disabled", 
    fg_color="#ffe066",   
    text_color="#ffffff"     
    )
    # spinner_label.grid(side="left", padx=(10, 0))
    spinner_label.pack(pady=(10, 0), anchor="center") 
    global spinner_animation_running, spinner_frame_index
    spinner_animation_running = True
    spinner_frame_index = 0
    # animate_spinner()
    start_spinner_animation()

    test_thread = threading.Thread(target=execute_test, args=(bank, pin, boa_rec_act, amount, etl_phone, safaricom_phone, bank_account, name))
    test_thread.start()


def execute_test(bank, pin, boa_rec_act, amount, etl_phone, safaricom_phone, bank_account, name):
    global test_process
    try:
        if not wait_for_appium_ready():
            log_message("Appium server is not ready.  Please check the Appium logs.")
            stop_spinner_animation()
            return


        python_executable = "python" 
        test_script_path = resource_path("test_app.py")  # Ensure this path is correct
        test_command = [
            python_executable,
            test_script_path,
            pin,
            name,
            boa_rec_act,
            amount,
            etl_phone,
            safaricom_phone,
            bank_account,
            bank
        ]

        if modular_checkbox_var.get():
            # test_command.append("modular")
            test_command.append(modular_var.get())
            if modular_var.get() == "Transfer":
                test_command.append(transfer_sub_var.get())

        log_message(f"Running test with command: {test_command}")
        test_process = subprocess.Popen(test_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  bufsize=1, universal_newlines=True, text=True)

        # Capture and display the output in real-time
        while True:
            if test_process.stdout:
                output = test_process.stdout.readline()
                if output:
                    log_message(output.strip())
            if test_process.stderr:
                error_output = test_process.stderr.readline()
                if error_output:
                    log_message(error_output.strip())
            if test_process.poll() is not None:
                break

        # Get the return code
        return_code = test_process.returncode
        log_message(f"Test script finished with return code: {return_code}")

        if return_code == 0:
            log_message("Test completed successfully.")
        else:
            log_message("Test failed.")

    except Exception as e:
        log_message(f"Error running test: {e}")
    finally:
        stop_spinner_animation()
        if test_process:
            test_process.kill()

def log_message(message):
    """
    Logs a message to the GUI log text area and the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message_with_timestamp = f"[{timestamp}] {message}\n"
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, log_message_with_timestamp)
    log_text.see(tk.END)  # Auto-scroll to the bottom
    log_text.config(state=tk.DISABLED)

    # Also write to the log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message_with_timestamp)

def stop_test():
    global test_process
    if test_process:
        log_message("Stopping test...")
        test_process.kill()
        test_process = None
        stop_spinner_animation()
        log_message("Test stopped.")
    else:
        log_message("No test is currently running.")

def start_spinner_animation():
    global spinner_animation_running, spinner_frame_index
    if not spinner_animation_running:
        spinner_animation_running = True
        spinner_frame_index = 0
        animate_spinner()

def stop_spinner_animation():
    global spinner_animation_running
    spinner_animation_running = False
    spinner_label.configure(image=spinner_frames[0] if spinner_frames else None)  # Reset to the first frame

# Load the spinner frames
spinner_frames = []
spinner_path = resource_path("spinner2.gif")
if os.path.exists(spinner_path):
    spinner_image = Image.open(spinner_path)
    for i in range(getattr(spinner_image, "n_frames", 1)):
        spinner_image.seek(i)
        frame = spinner_image.copy().resize((40, 40), Image.LANCZOS)
        spinner_frames.append(ImageTk.PhotoImage(frame))
else:
    print(f"Spinner image not found: {spinner_path}")

# Create the spinner label and initially set it to the first frame


# run_row_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
# run_row_frame.pack(pady=20)
# Create the buttons
button_frame = ctk.CTkFrame(left_frame, fg_color="#f5f5f5")
button_frame.pack(pady=20)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

spinner_label = tk.Label(button_frame, image=spinner_frames[0] if spinner_frames else None, bg="#f5f5f5")
spinner_label.pack(pady=(10, 0), anchor="center") 
# spinner_label.pack(side="left", padx=(10, 0))
spinner_label.pack_forget() 

run_button = ctk.CTkButton(
    button_frame,
    text="Run Test",
    command=run_test,
    font=("Arial", 16, "bold"),
    fg_color=logo_color,
    text_color="white",
    width=100,
    height=30,
    anchor="center",
    hover_color=logo_color
)
run_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

stop_button = ctk.CTkButton(
    button_frame,
    text="Stop Test",
    command=stop_test,
    font=("Arial", 16, "bold"),
    fg_color="#FF4500",  
    text_color="white",
    width=100,
    height=30,
    hover_color="#FF4500"
)
stop_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")



log_label = ctk.CTkLabel(
    right_frame,
    text="Test Log",
    font=("Arial", 18, "bold"),
    anchor="center",
    justify="center"
)
log_label.pack(pady=(10, 0), fill="x")

log_text = ScrolledText(
    right_frame,
    height=15,
    font=("Courier New", 8),  # Use a monospaced font for alignment
    bg="#f0f0f0",
    wrap=tk.WORD
)
log_text.pack(pady=10, fill="both", expand=True)
log_text.config(state=tk.DISABLED)  # Make it read-only

def on_closing():
    root.destroy()
    terminate_appium() 
    os._exit(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
