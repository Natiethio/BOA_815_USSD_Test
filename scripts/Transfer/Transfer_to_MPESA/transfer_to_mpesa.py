import unittest
import time
import re
import sys
import os


def transfer_to_mpesa(self):
        # print("Hello this is transfer_to_mpesa")
        print(self.pin)
        print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = self.transfer_helper()

        time.sleep(5)
        print("Test for transfer_to_mpesa ..", flush=True)

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

        status = self.send_ussd(expected_ResultB ,"4","transfer_to_mpesa")

        if not status:
            self.update_status("Transfer", [2], "Fail", 5)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Transfer", [2], "Pass", 5)

        message_text = self.get_ussd_message()

        #Enter invalid M-PESA Registered Number

        phone_et = self.phone_number
        status = self.send_ussd(expected_ResultC,phone_et,"transfer_to_mpesa")

        if not status:
            # self.driver.quit()
            # return
            print("Failed to send Phone for Transfer to M-PESA",flush=True)
            return


        #The entered M-PESA user should be verified and if it's not the system should throw an error accordingly

        message_text = self.get_ussd_message()
        status = self.send_ussd("This is not a registered M-PESA user.", "*", "M-PESA")

        if not status:
            print("The entered M-PESA user is not verified but the system is not throw an error ", flush=True)
            self.update_status("Transfer", [31], "Fail", 5)
        else:
            print("The entered M-PESA user is verified and the system is throw an error ", flush=True)
            self.update_status("Transfer", [31], "Pass", 5)
            time.sleep(0.5)

        #Selecting Transfer to M-PESA
        status = self.send_ussd(expected_ResultB ,"4","transfer_to_mpesa")

        #Enter valid M-PESA Registered Number

        phone_sf = self.safaricom_number
        status = self.send_ussd(expected_ResultC,phone_sf,"transfer_to_mpesa")

        if not status:
            # self.driver.quit()
            # return
            print("Failed to send Phone for Transfer to M-PESA",flush=True)
            return
        message_text = self.get_ussd_message()
        # Extract STAFF or SAVING account options
        account_option, account_number = self.extract_staff_or_saving_option(message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Transfer to M-PESA", account_option, "Transfer to M-PESA")

        if not status:
            print("Failed to select account", flush=True)
            return

        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        # Enter amount
        status = self.send_ussd("Enter Amount", 500100, "Transfer to M-PESA")

        if not status:
            print("Failed to send amount for Transfer to M-PESA", flush=True)
            return
        
        # Enter Remark
        status = self.send_ussd("Enter Remark", "Test", "Transfer to M-PESA")

        if not status:
            print("Failed to send Remark for Transfer to M-PESA", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "1", "M-PESA")

        if not status:
            print("Failed to send confirmatin for Transfer to M-PESA", flush=True)
            return
        #Attempt to transfer exceeding Maximum limit (>30,000) should not be applicable and throw error

        message_text = self.get_ussd_message()
        status = self.send_ussd("You have exceeded the single transaction limit.", "*", "M-PESA")

        if not status:
            print("airtime confirmation Should allow for >30,000", flush=True)
            self.update_status("Transfer", [32], "Fail", 5)
        else:
            print("airtime confirmation Should not allow for >30,000", flush=True)
            self.update_status("Transfer", [32], "Pass", 5)
            time.sleep(0.5)

        # test for positive Transfer to M-PESA

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Transfer to M-PESA")

        if not status:
            print("Failed to send amount for Transfer to M-PESA", flush=True)
            return
        
        # Enter Remark
        status = self.send_ussd("Enter Remark", "Test", "Transfer to M-PESA")

        if not status:
            print("Failed to send Remark for Transfer to M-PESA", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "M-PESA")

        if not status:
            print("M-PESA confirmation failed", flush=True)
            self.update_status("Transfer", [19], "Fail", 5)
        else:
            print(f"airtime confirmation pass for {account_number}", flush=True)
            self.update_status("Transfer", [19], "Pass", 5)
            time.sleep(0.5)


        print("Airtime transaction completed", flush=True)
        self.cancel_ussd()