import unittest
import time
import re
import sys
import os

def load_to_telebirr(self):
        # print("Hello this is load_to_telebirr")
        print(self.pin)
        print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = self.transfer_helper()

        time.sleep(5)
        print("Test for load_to_telebirr ..", flush=True)

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

        status = self.send_ussd(expected_ResultB ,"3","load_to_telebirr")

        if not status:
            self.update_status("Transfer", [2], "Fail", 5)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Transfer", [2], "Pass", 5)

        message_text = self.get_ussd_message()

        # Extract STAFF or SAVING account options
        account_option, account_number = self.extract_staff_or_saving_option(message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Load to TeleBirr", account_option, "Load to TeleBirr")

        if not status:
            print("Failed to select account", flush=True)
            return

        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", 30100, "Load to TeleBirr")

        if not status:
            print("Failed to send amount for Load to TeleBirr", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "1", "TeleBirr")

        if not status:
            print("Failed to send confirmatin for Load to TeleBirr", flush=True)
            return
        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        message_text = self.get_ussd_message()
        status = self.send_ussd("You have exceeded your telebirr transaction limit.", "*", "TeleBirr")

        if not status:
            print("airtime confirmation Should allow for >30,000", flush=True)
            self.update_status("Transfer", [23], "Fail", 5)
        else:
            print("airtime confirmation Should not allow for >30,000", flush=True)
            self.update_status("Transfer", [23], "Pass", 5)
            time.sleep(0.5)

        # test for positive load to telebirr

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "load to telebirr")

        if not status:
            print("Failed to send amount for load to telebirr", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "telebirr")

        if not status:
            print("telebirr confirmation failed", flush=True)
            self.update_status("Transfer", [19], "Fail", 5)
        else:
            print(f"airtime confirmation pass for {account_number}", flush=True)
            self.update_status("Transfer", [19], "Pass", 5)
            time.sleep(0.5)


        print("Airtime transaction completed", flush=True)
        self.cancel_ussd()

#testing for transfer_to_mpesa

