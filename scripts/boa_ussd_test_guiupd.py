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

    x = int((screen_width // 4) - (width // 4))
    y = int((screen_height // 4) - (height // 4))

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.update()

center_window(root, 1350, 700)

logo_color = "#f1ab15" 
#FFA500
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
    messagebox.showerror("Appium Error", "Appium is not ready. Please check the server.")
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
    "Exchange Rates": "7",
    # "Settings" : 8,
}

transfer_submodules = {
    "Transfer Within BOA": "1",
    "ATM Withdrawal": "2",
    "Load to TeleBirr": "3",
    "Transfer to M-PESA": "4",
    "Transfer(All)": "5"
}



transfer_with_otherbank = {
    "Instant Transfer" : "1",
    "Non Instant Transfer" : "2",
    "Transfer to Other Bank(All)" : "3"
}

airtime_submodules = {
    "EthioTelecom Airtime" : "1",
    "Safaricom Airtime" : "2",
    "Airtime(All)" : "3"
}

# Dictionary to hold input field widgets
input_fields = {}
fields = {}

bank_var = tk.StringVar(value="Select Bank")
modular_checkbox_var = tk.BooleanVar()
modular_var = tk.StringVar(value="Select Module")

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
name_row = create_input_field(form_frame, "Name")
boa_rec_act_row = create_input_field(form_frame, "BOA Receiver Act")
amount_row = create_input_field(form_frame, "Amount")
etl_phone_row = create_input_field(form_frame, "ETL Phone")
safaricom_phone_row = create_input_field(form_frame, "Safaricom Phone")
bank_account_row = create_input_field(form_frame, "Bank Account")


# Store the entry widgets in the 'fields' dictionary for easy access later
fields["PIN"] = input_fields["PIN"].winfo_children()[1]
fields["Name"] = input_fields["Name"].winfo_children()[1]
fields["BOA Receiver Act"] = input_fields["BOA Receiver Act"].winfo_children()[1]
fields["Amount"] = input_fields["Amount"].winfo_children()[1]
fields["ETL Phone"] = input_fields["ETL Phone"].winfo_children()[1]
fields["Safaricom Phone"] = input_fields["Safaricom Phone"].winfo_children()[1]
fields["Bank Account"] = input_fields["Bank Account"].winfo_children()[1]


# Create dropdowns and checkbox in column layout
bank_dropdown_row = ctk.CTkFrame(form_frame, fg_color="transparent")
bank_dropdown_row.pack(fill="x", pady=(5,5))
ctk.CTkLabel(bank_dropdown_row, text="Bank:", width=150, anchor="w", font=("Arial", 15, "bold")).pack(side="left", padx=(5, 2))
bank_dropdown = ctk.CTkOptionMenu(
    bank_dropdown_row,
    variable=bank_var,
    values=list(bank_options.keys()),
    width=250,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white"
)
bank_dropdown.pack(side="left", pady=3, ipady=4, padx=(2, 5), fill="x")

modular_checkbox_row = ctk.CTkFrame(form_frame, fg_color="transparent")
modular_checkbox_row.pack(anchor="w", pady=(5,5))
modular_checkbox = ctk.CTkCheckBox(
    modular_checkbox_row,
    text="Modular Test:",
    variable=modular_checkbox_var,
    font=("Arial", 15, "bold"),
    onvalue=True,
    offvalue=False,
    fg_color=logo_color,
    hover_color=logo_color
)
modular_checkbox.pack(side="left", padx=(5, 2))

modular_dropdown = ctk.CTkOptionMenu(
    modular_checkbox_row,
    variable=modular_var,
    values=list(test_options.keys()),
    width=100, 
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white"
)
modular_dropdown.pack(side="left", padx=(5, 2))
modular_dropdown.pack_forget()  

transfer_sub_var = tk.StringVar(value="Select")

transfer_sub_dropdown = ctk.CTkOptionMenu(
    modular_checkbox_row,
    variable=transfer_sub_var,
    values=list(transfer_submodules.keys()),
    width=100,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=transfer_sub_var.set
)
transfer_sub_dropdown.pack(side="left", padx=(5, 2))
transfer_sub_dropdown.pack_forget()  


transfer_with_otherbank_sub_var = tk.StringVar(value="Select")

transfer_with_otherbank_dropdown = ctk.CTkOptionMenu(
    modular_checkbox_row,
    variable=transfer_with_otherbank_sub_var,
    values=list(transfer_with_otherbank.keys()),
    width=100,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=transfer_with_otherbank_sub_var.set
)

transfer_with_otherbank_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 2))
transfer_with_otherbank_dropdown.pack_forget() 

airtime_sub_var = tk.StringVar(value="Select")
airtime_sub_dropdown = ctk.CTkOptionMenu(
    modular_checkbox_row,
    variable=airtime_sub_var,
    values=list(airtime_submodules.keys()),
    width=100,
    font=("Arial", 15),
    fg_color=logo_color,
    button_color=logo_color,
    button_hover_color=logo_color,
    text_color="white",
    command=airtime_sub_var.set
)

airtime_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 2))
airtime_sub_dropdown.pack_forget() 

def update_input_fields():

    for row in [pin_row, name_row, boa_rec_act_row, amount_row, etl_phone_row, safaricom_phone_row, bank_account_row]:
        row.pack_forget()


    bank_dropdown_row.pack_forget()
    bank_dropdown.pack_forget()

    if not modular_checkbox_var.get():
        pin_row.pack(fill="x", pady=(5,5))
        boa_rec_act_row.pack(fill="x", pady=(5,5))
        amount_row.pack(fill="x", pady=(5,5))
        etl_phone_row.pack(fill="x", pady=(5,5))
        safaricom_phone_row.pack(fill="x", pady=(5,5))
        bank_account_row.pack(fill="x", pady=(5,5))
        name_row.pack(fill="x", pady=(5,5))
        bank_dropdown_row.pack(side="left", padx=(5, 2))
        bank_dropdown.pack(side="left", pady=3, ipady=4, padx=(2, 5), fill="x")
        bank_var.set("Select Bank")
    else:
        selected_module = modular_var.get()
        if selected_module == "My Accounts":
            pin_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Transfer":
            pin_row.pack(fill="x", pady=(5,5))
            selected_submodule_text = transfer_sub_var.get()
            print(selected_submodule_text)
            if selected_submodule_text == "Transfer Within BOA":
                boa_rec_act_row.pack(fill="x", pady=(5,5))
                amount_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "ATM Withdrawal":
                pass  # Only PIN is needed
            elif selected_submodule_text == "Load to TeleBirr":
                amount_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "Transfer to M-PESA":
                amount_row.pack(fill="x", pady=(5,5))
                # etl_phone_row.pack(fill="x", pady=(5,5))
                safaricom_phone_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text == "Transfer(All)":
                boa_rec_act_row.pack(fill="x", pady=(5,5))
                amount_row.pack(fill="x", pady=(5,5))
                etl_phone_row.pack(fill="x", pady=(5,5))
                safaricom_phone_row.pack(fill="x", pady=(5,5))

        elif selected_module == "Transfer to Other Bank":

            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
    
            selected_submodule_text2 = transfer_with_otherbank_sub_var.get()
            print(selected_submodule_text2)
            if selected_submodule_text2 == "Instant Transfer":
                bank_account_row.pack(fill="x", pady=(5,5))
                bank_dropdown_row.pack(side="left", padx=(5, 2))
                bank_dropdown.pack(side="left", pady=3, ipady=4, padx=(2, 5), fill="x")
            if selected_submodule_text2 == "Non Instant Transfer" or selected_submodule_text2 == "Transfer to Other Bank(All)":
                bank_account_row.pack(fill="x", pady=(5,5))
                name_row.pack(fill="x", pady=(5,5))
                bank_dropdown_row.pack(side="left", padx=(5, 2))
                bank_dropdown.pack(side="left", pady=3, ipady=4, padx=(2, 5), fill="x")
        elif selected_module == "Transfer to Own":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Airtime":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
            selected_submodule_text3 = airtime_sub_var.get()
            print(selected_submodule_text3)
            if selected_submodule_text3 == "EthioTelecom Airtime":
                etl_phone_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text3 == "Safaricom Airtime":
                safaricom_phone_row.pack(fill="x", pady=(5,5))
            elif selected_submodule_text3 == "Airtime(All)":
                etl_phone_row.pack(fill="x", pady=(5,5))
                safaricom_phone_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Utilities":
            pin_row.pack(fill="x", pady=(5,5))
            amount_row.pack(fill="x", pady=(5,5))
            etl_phone_row.pack(fill="x", pady=(5,5))
            safaricom_phone_row.pack(fill="x", pady=(5,5))
        elif selected_module == "Exchange Rates":
            pin_row.pack(fill="x", pady=(5,5))

    # Only pack bank_row at the end if modular test is not checked
    if not modular_checkbox_var.get():
        bank_dropdown_row.pack_forget()
        bank_dropdown_row.pack(fill="x", pady=(5,5), anchor="w")

def toggle_modular_dropdown():
    if modular_checkbox_var.get():
        modular_dropdown.pack(side="left", pady=3, ipady=4 , padx=(5, 2))
        if modular_var.get() == "Transfer":
            transfer_sub_dropdown.pack(side="left", padx=(5, 2))
        else:
            transfer_sub_dropdown.pack_forget()
    else:
        modular_dropdown.pack_forget()
        transfer_sub_dropdown.pack_forget()
        transfer_with_otherbank_dropdown.pack_forget()
        airtime_sub_dropdown.pack_forget()
        modular_var.set("Select Module")
        transfer_sub_var.set("Select")
        transfer_with_otherbank_sub_var.set("Select")
        airtime_sub_var.set("Select")

    update_input_fields()

modular_checkbox.configure(command=toggle_modular_dropdown)

def on_modular_change(*args):
    if modular_var.get() == "Transfer":
        # transfer_sub_dropdown.pack(side="left", padx=(5, 2))
        transfer_sub_var.set("Select")
        transfer_with_otherbank_dropdown.pack_forget()
        airtime_sub_dropdown.pack_forget()
        transfer_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 2))
    elif modular_var.get() == "Transfer to Other Bank":
         transfer_with_otherbank_sub_var.set("Select")
         transfer_sub_dropdown.pack_forget()
         airtime_sub_dropdown.pack_forget()
         transfer_with_otherbank_dropdown.pack(side="left", pady=3, ipady=4, padx=(10, 0))
    elif modular_var.get() == "Airtime":
        airtime_sub_var.set("Select")
        transfer_sub_dropdown.pack_forget()
        transfer_with_otherbank_dropdown.pack_forget()
        airtime_sub_dropdown.pack(side="left", pady=3, ipady=4, padx=(5, 2))
    else:
        # modular_dropdown.pack_forget()
        # modular_var.set("Select Module")
        transfer_sub_dropdown.pack_forget()
        transfer_sub_var.set("Select")
        transfer_with_otherbank_dropdown.pack_forget()
        transfer_with_otherbank_sub_var.set("Select")
        airtime_sub_dropdown.pack_forget()
        airtime_sub_var.set("Select")

    update_input_fields()


    
modular_var.trace_add("write", on_modular_change)
transfer_sub_var.trace_add("write", lambda *args: update_input_fields())
transfer_with_otherbank_sub_var.trace_add("write", lambda *args: update_input_fields())
airtime_sub_var.trace_add("write", lambda *args: update_input_fields())
modular_checkbox_var.trace_add("write", lambda *args: update_input_fields())

def is_valid_numeric(value):
    try:
      if value != "0" and value.isdigit() and  float(value):
        return True
      else:
        return False
    except ValueError:
        return False

def get_field_values():

    values = {}
    for field_name in ["PIN", "Name", "BOA Receiver Act", "Amount", "ETL Phone", "Safaricom Phone", "Bank Account"]:
        try:
            # Try to get the value.  If the widget doesn't exist, we assume
            # the field is not relevant to the current test and use a default.
            values[field_name] = fields[field_name].get()
        except KeyError:
            values[field_name] = ""  # Or some other default value
    return values

def run_test():
    # print("Run Test button pressed")
    run_button.configure(state="disabled")  
    spinner_label.grid() 
    stop_button.grid()
    bank = bank_var.get()

    if bank == "Select Bank":
    #   print(bank)
      bank = bank_var.get()
    else:
      bank = bank_options[bank_var.get()] 
    #   print(bank)


    field_values = get_field_values()
    pin = field_values["PIN"]
    name = field_values["Name"]
    boa_rec_act = field_values["BOA Receiver Act"]
    amount = field_values["Amount"]
    etl_phone = field_values["ETL Phone"]
    safaricom_phone = field_values["Safaricom Phone"]
    bank_account = field_values["Bank Account"]


    if not modular_checkbox_var.get():

        if not pin:
            show_validation_error("Error: PIN is required.")
            return
        
        if not validate_Pin(pin):
            show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
            return
        
        if not name:
            show_validation_error("Error: Name is required.")
            return
        
        if not is_valid_alphabet(name):
            show_validation_error(f"{name} Validation Error: Name must contain only alphabetic characters")
            return           
        
        if not boa_rec_act:
            show_validation_error("Error:BOA Receiver Account is required.")
            return
        
        if not validate_BOA_Account(boa_rec_act):
            show_validation_error(f"{boa_rec_act} Validation Error: Invalid BOA Receiver Account")
            return
        
        if not amount:
            show_validation_error("Error:Amount is required.")
            return
        
        if not is_valid_numeric(amount):
            show_validation_error("Error:Amount must be a valid number.")
            return
        
        if not etl_phone:
            show_validation_error("Error: EthioTelecom Phone is required.")
            return
        
        if not validate_ETL(etl_phone):
            show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
            return
        
        if not safaricom_phone:
            show_validation_error("Error: Safaricom Phone is required.")
            return
        
        if not validate_Saf(safaricom_phone):
            show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
            return
        
        if not bank_account:
            show_validation_error("Error: Bank Account is required.")
            return
        

    if modular_checkbox_var.get():
        selected_module = modular_var.get()
        if selected_module == "Select Module":
            show_validation_error("Error: Please select a module.")
            return

        if selected_module == "My Accounts":
            if not pin:
                show_validation_error("Error: PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
            
        elif selected_module == "Transfer":

            selected_submodule = transfer_sub_var.get()

            if selected_submodule == "Select":
                show_validation_error("Error: Please select a transfer submodule.")
                return
            
            if not pin:
                show_validation_error("Error: PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return

            if selected_submodule == "Transfer Within BOA":
                if not boa_rec_act:
                    show_validation_error("Error: BOA Receiver Account is required.")
                    return
                
                if not validate_BOA_Account(boa_rec_act):
                   show_validation_error(f"{boa_rec_act} Validation Error: Invalid BOA Receiver Account")
                   return
                       
                if not amount:
                    show_validation_error("Error: Amount is required.")
                    return
                
                if not is_valid_numeric(amount):
                    show_validation_error("Error: Amount must be a valid number.")
                    return
                
                
            elif selected_submodule == "Load to TeleBirr":
                
                if not amount:
                    show_validation_error("Error: Amount is required.")
                    return
                
                if not is_valid_numeric(amount):
                    show_validation_error("Error: Amount must be a valid number.")
                    return
                
            elif selected_submodule == "Transfer to M-PESA":

                if not amount:
                    show_validation_error("Error: Amount is required.")
                    return
                
                if not is_valid_numeric(amount):
                    show_validation_error("Error: Amount must be a valid number.")
                    return
             
                if not safaricom_phone:
                        show_validation_error("Error: Safaricom Phone is required.")
                        return
                
                if not validate_Saf(safaricom_phone):
                        show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                        return 
                
            elif selected_submodule == "Transfer(All)":
          
                if not boa_rec_act:
                    show_validation_error("Error: BOA Receiver Account is required.")
                    return
                
                if not validate_BOA_Account(boa_rec_act):
                    show_validation_error(f"{boa_rec_act} Validation Error: Invalid BOA Receiver Account")
                    return                    
                
                if not amount:
                    show_validation_error("Error: Amount is required.")
                    return
                
                if not is_valid_numeric(amount):
                    show_validation_error("Error: Amount must be a valid number.")
                    return
                
                if not etl_phone:
                    show_validation_error("Error: ETL Phone is required.")
                    return
                
                if not validate_ETL(etl_phone):
                    show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
                    return
                              
                if not safaricom_phone:
                    show_validation_error("Error: Safaricom Phone is required.")
                    return
                
                if not validate_Saf(safaricom_phone):
                    show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                    return             

        elif selected_module == "Transfer to Other Bank":
            selected_otherbank_submodule= transfer_with_otherbank_sub_var.get()

            if selected_otherbank_submodule == "Select":
                show_validation_error("Error: Please select a transfer to other bank submodule.")
                return 
            
            if not pin:
                show_validation_error("Error: PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return

            if not amount:
                show_validation_error("Error: Amount is required.")
                return
            
            if not is_valid_numeric(amount):
                show_validation_error("Error: Amount must be a valid number.")
                return

            if not bank_account:
                show_validation_error("Error: Bank Account is required.")
                return          


            if selected_otherbank_submodule == "Non Instant Transfer" or selected_otherbank_submodule == "Transfer to Other Bank(All)":

                if not name:
                    show_validation_error("Error: Name is required.")
                    return
                
                if not is_valid_alphabet(name):
                    show_validation_error(f"{name} Validation Error: Name must contain only alphabetic characters")
                    return 

        elif selected_module == "Transfer to Own":
            if not pin:
                show_validation_error("Error:PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
            
            if not amount:
                show_validation_error("Error:Amount is required.")
                return
            
            if not is_valid_numeric(amount):
                show_validation_error("Error:Amount must be a valid number.")
                return
                       

        elif selected_module == "Airtime":
            selected_submodule = airtime_sub_var.get()
            if selected_submodule == "Select":
                show_validation_error("Error: Please select a airtime submodule.")
                return
            
            if not pin:
                show_validation_error("Error:PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
            
            if not amount:
                show_validation_error("Error:Amount is required.")
                return
            
            if not is_valid_numeric(amount):
                show_validation_error("Error:Amount must be a valid number.")
                return
            
            if selected_submodule == "EthioTelecom Airtime":
              
              if not etl_phone:
                 show_validation_error("Error:ETL Phone is required.")
                 return
            
              if not validate_ETL(etl_phone):
                    show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
                    return
                
            elif selected_submodule == "Safaricom Airtime":
              
              if not safaricom_phone:
                  show_validation_error("Error:Safaricom Phone is required.")
                  return
            
              if not validate_Saf(safaricom_phone):
                    show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                    return
              
            elif selected_submodule == "Airtime(All)":

                if not etl_phone:
                    show_validation_error("Error:ETL Phone is required.")
                    return
                
                if not validate_ETL(etl_phone):
                    show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
                    return
                
                if not safaricom_phone:
                    show_validation_error("Error:Safaricom Phone is required.")
                    return
                
                if not validate_Saf(safaricom_phone):
                    show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                    return
            
        elif selected_module == "Utilities":
            if not pin:
                show_validation_error("Error:PIN is required.")
                return
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
            if not boa_rec_act:
                show_validation_error("Error:BOA Receiver Account is required.")
                return
            if not validate_BOA_Account(boa_rec_act):
                show_validation_error(f"{boa_rec_act} Validation Error: Invalid BOA Receiver Account")
                return     
            if not amount:
                show_validation_error("Error:Amount is required.")
                return
            if not is_valid_numeric(amount):
                show_validation_error("Error:Amount must be a valid number.")
                return
            if not etl_phone:
                show_validation_error("Error:ETL Phone is required.")
                return
            
            if not validate_ETL(etl_phone):
                    show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
                    return
                
            if not safaricom_phone:
                show_validation_error("Error:Safaricom Phone is required.")
                return
            
            if not validate_Saf(safaricom_phone):
                    show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                    return
            
        elif selected_module == "Exchange Rates":
            if not pin:
                show_validation_error("Error:PIN is required.")
                return
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
              
    if modular_checkbox_var.get():
        selected_module = modular_var.get()
        selected_otherbank_submodule = transfer_with_otherbank_sub_var.get()
        if selected_module == "Transfer to Other Bank":
            if bank == "Select Bank":
                show_validation_error("Please select bank.")
                return   
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin} Validation Error: PIN must contain only only four number characters")
                return
        
            if(selected_otherbank_submodule == "Non Instant Transfer"):

                if not is_valid_alphabet(name):
                    show_validation_error(f"{name} Validation Error: Name must contain only alphabetic characters")
                    return
            
            if not is_valid_integer(amount):
                    show_validation_error(f"{amount} Validation Error: Amount must be an integer")
                    return
                
            
            if bank == "1" and not validate_cbe(bank_account):
                show_validation_error("Invalid CBE Account.")
                return

            if bank == "2" and not validate_awash(bank_account):
                show_validation_error("Invalid Awash Account.")
                return

            if bank == "3" and not validate_dashen(bank_account):
                show_validation_error("Invalid Dashen Account.")
                return
                
    else:
            if bank == "Select Bank":
                show_validation_error("Please select bank.")
                return   
            
            if not validate_Pin(pin):
                show_validation_error(f"{pin}Validation Error: PIN must contain only only four number characters")
                return
        
            
            if not is_valid_integer(amount):
                    show_validation_error(f"{amount} Validation Error: Amount must be an integer")
                    return
                
            if not validate_BOA_Account(boa_rec_act):
                    show_validation_error(f"{boa_rec_act} Validation Error: Invalid BOA Receiver Account")
                    return
                
            if not validate_ETL(etl_phone):
                    show_validation_error(f"{etl_phone} Validation Error: Invalid ethio telecom number")
                    return
                
            if not validate_Saf(safaricom_phone):
                    show_validation_error(f"{safaricom_phone} Validation Error: Invalid safaricom number")
                    return
            
            if bank == "1" and not validate_cbe(bank_account):
                show_validation_error("Invalid CBE Account.")
                return

            if bank == "2" and not validate_awash(bank_account):
                show_validation_error("Invalid Awash Account.")
                return

            if bank == "3" and not validate_dashen(bank_account):
                show_validation_error("Invalid Dashen Account.")
                return
         
    start_spinner_animation()
    test_thread = threading.Thread(target=execute_test, args=(pin, name, boa_rec_act, amount, etl_phone, safaricom_phone, bank_account, bank), daemon=True)
    test_thread.start()


def show_validation_error(message):
    spinner_label.grid_remove()
    stop_button.grid_remove()
    root.update_idletasks()
    messagebox.showerror("Validation Error", message)
    run_button.configure(state="normal")

def execute_test( pin, name, boa_rec_act, amount, etl_phone, safaricom_phone, bank_account, bank):
    global test_process
    try:
        log_output.delete("1.0", tk.END)

        if not wait_for_appium_ready():
            log_message("Appium server is not ready.  Please check the Appium logs.")
            stop_spinner_animation()
            run_button.configure(state="normal") 
            spinner_label.grid_remove()  
            stop_button.grid_remove()  
            return


        python_executable = "python" 
        # test_script_path = resource_path("test_app.py")  
        test_script_path = resource_path("test_runner.exe") 

        if not os.path.exists(test_script_path):
            messagebox.showerror("File Error", "test_runner.exe or test_app not found.")
            return
        
        test_command = [
            # python_executable,
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

            # selected_module = test_options[modular_var.get()]
            # test_command.append(selected_module)
            test_command.append(test_options[modular_var.get()])
            if modular_var.get() == "Transfer":
                test_command.append(transfer_submodules[transfer_sub_var.get()])
            elif modular_var.get() == "Transfer to Other Bank":
                test_command.append("")
                test_command.append(transfer_with_otherbank[transfer_with_otherbank_sub_var.get()])
            elif modular_var.get() == "Airtime":
                test_command.append("")
                test_command.append("")
                test_command.append(airtime_submodules[airtime_sub_var.get()])
        # log_message(f"Running test with command: {test_command}")
        print(f"Running test with command: {test_command}")

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        separator = f"\n{'='*17}  New Test Started at {timestamp}  {'='*17}\n"
        log_output.insert(tk.END, separator)
        log_output.see(tk.END)
        write_to_logfile(separator)

        test_process = subprocess.Popen(test_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)

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
        stop_spinner_animation()
        log_output.see(tk.END)
        if test_process:
            test_process.kill()
        run_button.configure(state="normal")  
        spinner_label.grid_remove()  
        stop_button.grid_remove()  

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
    return pin.isdigit() and  len(pin) == 4

def is_valid_alphabet(value):
    return value.isalpha()

def is_valid_integer(value):
    return value.isdigit()


def log_message(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message_with_timestamp = f"[{timestamp}] {message}\n"
    log_output.config(state=tk.NORMAL)
    # log_text.insert(tk.END, log_message_with_timestamp)
    # log_text.see(tk.END)  # Auto-scroll to the bottom
    # log_text.config(state=tk.DISABLED)

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
        run_button.configure(state="normal")  # Re-enable run button when test stops
        spinner_label.grid_remove()  # Hide the spinner
        stop_button.grid_remove()  # Hide the stop button
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

# Create the buttons
button_frame = ctk.CTkFrame(left_frame, fg_color="#f5f5f5")
button_frame.pack(side="bottom", pady=20, fill="x")  # Changed to pack at bottom of left_frame
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

run_button = ctk.CTkButton(
    button_frame,
    text="Run Test",
    command=run_test,
    font=("Arial", 16, "bold"),
    fg_color=logo_color,
    text_color="white",
    hover_color=logo_color,
    width=120, # Set fixed width
    height=30
)
run_button.grid(row=0, column=0, padx=(0, 10), sticky="e")

# Create the spinner label and initially set it to the first frame
spinner_label = tk.Label(button_frame, image=spinner_frames[0] if spinner_frames else None, bg="#f5f5f5")
spinner_label.grid(row=0, column=1, padx=10)
spinner_label.grid_remove()  # Initially hide the spinner

stop_button = ctk.CTkButton(
    button_frame,
    text="Stop Test",
    command=stop_test,
    font=("Arial", 16, "bold"),
    fg_color="#FF4500",  # Orange Red
    text_color="white",
    hover_color="#FF4500",
    width=120,  # Set fixed width
    height=30
)
stop_button.grid(row=0, column=2, padx=(10, 0), sticky="w")
stop_button.grid_remove()  # Initially hide the stop button



log_label = ctk.CTkLabel(
    right_frame,
    text="Test Log",
    font=("Arial", 18, "bold"),
    anchor="center",
    justify="center"
)
log_label.pack(pady=(10, 0), fill="x")


log_output = ScrolledText(right_frame, height=20, font=("Courier", 8) ,wrap=tk.WORD)
log_output.pack(fill="both", expand=True)

def on_closing():
    root.destroy()
    terminate_appium() 
    os._exit(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI main loop
root.mainloop()
# terminate_appium()
# pyinstaller --onefile --noconsole --add-data "My_Account;My_Account"  --add-data "Transfer;Transfer" --add-data "Transfer_otherBank;Transfer_otherBank"  --add-data "Transfer_to_own;Transfer_to_own" --add-data "AirTime;AirTime" --add-data "Exchange_Rates;Exchange_Rates" --add-data "Helpers;Helpers" --add-data "USSD_Test_Script.xlsx;." --name "test_runner" test_app.py

# pyinstaller --onefile --noconsole --add-data "test_runner.exe;." --add-data "logo.png;." --add-data "spinner2.gif;."  --add-data "USSD_Test_Script.xlsx;." --icon=logo_icon.ico --name="ussd815_tester" --distpath=dist_gui  --workpath=build_gui  boa_ussd_test_guiupd.py

