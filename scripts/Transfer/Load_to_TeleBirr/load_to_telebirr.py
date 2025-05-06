import unittest
import time
import re
import sys
import os
from Helpers.transfer_helper import transfer_helper
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option

def load_to_telebirr(self):
        # print("Hello this is load_to_telebirr")
        # print(self.pin)
        # print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = transfer_helper(self)

        time.sleep(5)
        print("Test for Load to Telebirr ..", flush=True)

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            load_to_telebirr(self)
            return
                
        expected_ResultB = [
            "Transfer",
            "1: Transfer within BoA", 
            "2: ATM withdrawal",
            "3: Load to TeleBirr",
            "4: Transfer to M-PESA",
            "5: Awach"
            ]
        
        
        
        expected_ResultC = [ 
            "Load to TeleBirr"
        ]
                
        # WebDriverWait(self.driver, 20).until(
        # EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_ResultB ,"3","load_to_telebirr", "BoA Accounts List Page(Load to TeleBirr)")

        if not status:
            self.update_status("Transfer", [2], "Fail", 5)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Transfer", [2], "Pass", 5)

        message_text = self.get_ussd_message()

        # Extract STAFF or SAVING account options
        account_option, account_number = extract_staff_or_saving_option(self, message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Load to TeleBirr", account_option, "Load to TeleBirr", "Enter Amount Page")

        if not status:
            print("Failed to select account", flush=True)
            return

        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        # Enter amount
        print("Testing telebirr over limit(>30,000) Case")
        amount = self.amount
        status = self.send_ussd("Enter Amount", 30100, "Load to TeleBirr", "Confirmation Page")

        if not status:
            print("Failed to send amount for Load to TeleBirr", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "1", "TeleBirr", "TeleBirr limit exceed page")

        if not status:
            print("Failed to send confirmatin for Load to TeleBirr", flush=True)
            return
        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        message_text = self.get_ussd_message()
        status = self.send_ussd("You have exceeded your telebirr transaction limit.", "*", "TeleBirr","Enter Amount Page(Back Navigated)")

        if not status:
            print("Error: Load to TeleBirr confirmation is allowing for transfer >30,000", flush=True)
            self.update_status("Transfer", [23], "Fail", 5)
        else:
            print("Load to TeleBirr confirmation should not allow for >30,000", flush=True)
            self.update_status("Transfer", [23], "Pass", 5)
            time.sleep(0.5)



        # Enter amount
        print("Test for Positive Scenario For TeleBirr Transfer", flush=True)
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "load to telebirr", "Confirmation Page")

        if not status:
            print("Failed to send amount for load to telebirr", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "telebirr")

        if not status:
            print("TeleBirr confirmation failed", flush=True)
            self.update_status("Transfer", [19], "Fail", 5)
            self.cancel_ussd()
            return False
        else:
            print(f"TeleBirr confirmation pass for {account_number}", flush=True)
            self.update_status("Transfer", [19], "Pass", 5)
            print("Load to Telebirr transaction completed", flush=True)
            print_and_clear_slow_popups(self, "Load to TeleBirr")
            self.cancel_ussd()
            return True

def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()



