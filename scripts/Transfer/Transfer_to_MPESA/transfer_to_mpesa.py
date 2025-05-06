import unittest
import time
import re
import sys
import os
from Helpers.transfer_helper import transfer_helper
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option

def transfer_to_mpesa(self):
        # print("Hello this is transfer_to_mpesa")
        # print(self.pin)
        # print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = transfer_helper(self)

        time.sleep(5)
        print("Test for Transfer to M-PESA ..", flush=True)

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            transfer_to_mpesa(self)
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
            "Enter M-PESSA Registered Number"
        ]
                
        # WebDriverWait(self.driver, 20).until(
        # EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_ResultB ,"4","transfer_to_mpesa", "Enter M-PESA Registerd Phone")

        if not status:
            self.update_status("Transfer", [2], "Fail", 5)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Transfer", [2], "Pass", 5)

        #Enter invalid M-PESA Registered Number
        print("Testing for not verified M-PESA user by using invalid M-PESA user phone number", flush=True)
        phone_test = self.etl_number
        status = self.send_ussd(expected_ResultC, phone_test,"Transfer_to_M-PESA", "Not verified M-PESA User Page")

        if not status:
            # self.driver.quit()
            # return
            print("Failed to send Phone for Transfer to M-PESA",flush=True)
            return



        status = self.send_ussd("This is not a registered M-PESA user.", "*", "M-PESA", "Transfer Home Page(Back Navigated)")

        if not status:
            print("The entered M-PESA user is not valid but the system is not throwing an error ", flush=True)
            self.update_status("Transfer", [31], "Fail", 5)
            return
        else:
            print("The entered M-PESA user is valid and the system is throwing an error ", flush=True)
            self.update_status("Transfer", [31], "Pass", 5)
            # self.send_ussd_input("*")
            time.sleep(0.5)

        #Selecting Transfer to M-PESA
        status = self.send_ussd(expected_ResultB ,"4","transfer_to_mpesa", "Enter M-PESA Registerd Phone")

        #Enter valid M-PESA Registered Number

        phone_sf = self.safaricom_number
        status = self.send_ussd(expected_ResultC,phone_sf,"transfer_to_mpesa", "BOA Accounts List Page")

        if not status:
            # self.driver.quit()
            # return
            print("Failed to send Phone for Transfer to M-PESA",flush=True)
            return
        message_text = self.get_ussd_message()
        # Extract STAFF or SAVING account options
        account_option, account_number = extract_staff_or_saving_option(self, message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Transfer to M-PESA", account_option, "Transfer to M-PESA", "Enter Amount Page")

        if not status:
            print("Failed to select account", flush=True)
            return

        print("Testing overlimit M-PESA transfer scenario", flush=True)

        status = self.send_ussd("Enter Amount", 500100, "Transfer to M-PESA", "Enter Remark Page")

        if not status:
            print("Failed to send amount for Transfer to M-PESA", flush=True)
            return
        
        # Enter Remark
        status = self.send_ussd("Enter Remark", "Test", "Transfer to M-PESA", "Confiramtion Page")

        if not status:
            print("Failed to send Remark for Transfer to M-PESA", flush=True)
            return
    

        status = self.send_ussd("Please Confirm", "1", "M-PESA", "Single Transaction Exceeded Limit Page")

        if not status:
            print("Failed to send confirmatin for Transfer to M-PESA", flush=True)
            return
        

        status = self.send_ussd("You have exceeded the single transaction limit.", "*", "M-PESA", "Enter Amount(Back Navigated)")

        if not status:
            print("Transfer to M-PESA confirmation Should allow for >30,000", flush=True)
            self.update_status("Transfer", [32], "Fail", 5)
        else:
            print("Transfer to M-PESA confirmation Should not allow for >30,000", flush=True)
            self.update_status("Transfer", [32], "Pass", 5)
            time.sleep(0.5)

        print("Test for Positive Scenario For M-PESA Transfer", flush=True)

        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Transfer to M-PESA", "Enter Remark Page")

        if not status:
            print("Failed to send amount for Transfer to M-PESA", flush=True)
            return
        
        # Enter Remark
        status = self.send_ussd("Enter Remark", "Test", "Transfer to M-PESA", "Confiramtion Page")

        if not status:
            print("Failed to send Remark for Transfer to M-PESA", flush=True)
            return
        
         
        status = self.send_ussd("Please Confirm", "*", "M-PESA")

        if not status:
            print("Transfer to M-PESA confirmation failed", flush=True)
            self.update_status("Transfer", [27], "Fail", 5)
            self.cancel_ussd()
            return False
        else:
            print(f"Transfer to M-PESA confirmation pass for {account_number}", flush=True)
            self.update_status("Transfer", [27], "Pass", 5)
            print("Transfer to M-PESA transaction completed", flush=True)
            print_and_clear_slow_popups(self, "Transfer to M-PESA")
            self.cancel_ussd()
            return True



def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()