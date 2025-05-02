import unittest
import time
import re
import sys
import os

def airtime_topup_for_ethio_telecom(self):
        print("Hello this is airtime ext")
        print(self.pin)
        print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = self.airtime_helper()

        time.sleep(5)
        print("Test for Airtime ..", flush=True)

        # status_helper = self.airtime_helper()

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            airtime_topup_for_ethio_telecom(self)
            return
                
        expected_ResultB = [
            "Airtime",
            "1: EthioTelecom Airtime", 
            "2: Safaricom Airtime",
            ]
        
        
        
        expected_ResultC = [ 
            "EthioTelecom Airtime"
        ]
                
        # WebDriverWait(self.driver, 20).until(
        # EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_ResultB ,"1","EthioTelecom Airtime")

        if not status:
            self.update_status("Airtime topup", [2], "Fail", 7)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Airtime topup", [2], "Pass", 7)

        message_text = self.get_ussd_message()

        # Extract STAFF or SAVING account options
        account_option, account_number = self.extract_staff_or_saving_option(message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("EthioTelecom Airtime", account_option, "EthioTelecom Airtime")

        if not status:
            print("Failed to select account", flush=True)
            return

        # Enter phone invalid number 
        phone_sf = self.safaricom_number
        print(f"Entering phone number {phone_sf}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_sf , "EthioTelecom Airtime")

        if not status:
            print("Failed to send phone for EthioTelecom Airtime", flush=True)
            return

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "EthioTelecom Airtime")

        if not status:
            print("Failed to send amount for EthioTelecom Airtime", flush=True)
            return

        # Confirm transaction
        message_text = self.get_ussd_message()
        status = self.send_ussd("Please Confirm", "1", "airtime")

        if not status:
            print("Failed to send confirmatin for EthioTelecom Airtime", flush=True)
            return
        #invalid pfone Ethio Telecom phone No
        message_text = self.get_ussd_message()
        status = self.send_ussd("(Ex: 09xxxxxxxx)", "*", "airtime")
        
        if not status:
            print("Detecting Invalid phone number is  failed", flush=True)
            self.update_status("Airtime topup", [9], "Fail", 7)
        else:
            print(f"Detecting Invalid phone number is pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [9], "Pass", 7)

        # Enter valid phone number
        phone_et = self.phone_number
        print(f"Entering phone number {phone_et}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_et , "EthioTelecom Airtime")

        if not status:
            print("Failed to send phone for EthioTelecom Airtime", flush=True)
            return
        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "EthioTelecom Airtime")

        if not status:
            print("Failed to send amount for EthioTelecom Airtime", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "airtime")

        if not status:
            print("airtime confirmation failed", flush=True)
            self.update_status("Airtime topup", [5], "Fail", 7)
        else:
            print(f"airtime confirmation pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [5], "Pass", 7)
            time.sleep(0.5)


        print("Airtime transaction completed", flush=True)
        self.cancel_ussd()

        #testing for airtime topup for safaricom


def airtime_topup_for_safaricom(self):
        print("Hello this is airtime ext")
        print(self.pin)
        print(self.phone_number)

        self.enter_pin_to_login()

        status_helper = self.airtime_helper()

        time.sleep(5)
        print("Test for Airtime ..", flush=True)

        # status_helper = self.airtime_helper()

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            airtime_topup_for_safaricom(self)
            return
                
        expected_ResultB = [
            "Airtime",
            "1: EthioTelecom Airtime", 
            "2: Safaricom Airtime",
            ]
        
        
        
        expected_ResultC = [ 
            "Safaricom Airtime"
        ]
                
        # WebDriverWait(self.driver, 20).until(
        # EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_ResultB ,"2","Safaricom Airtime")

        if not status:
            self.update_status("Airtime topup", [2], "Fail", 7)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Airtime topup", [2], "Pass", 7)

        message_text = self.get_ussd_message()

        # Extract STAFF or SAVING account options
        account_option, account_number = self.extract_staff_or_saving_option(message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Safaricom Airtime", account_option, "Safaricom Airtime")

        if not status:
            print("Failed to select account", flush=True)
            return

        # Enter phone invalid number 
        phone_et = self.phone_number
        print(f"Entering phone number {phone_et}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_et , "Safaricom Airtime")

        if not status:
            print("Failed to send phone for Safaricom Airtime", flush=True)
            return

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Safaricom Airtime")

        if not status:
            print("Failed to send amount for Safaricom Airtime", flush=True)
            return

        # Confirm transaction
        message_text = self.get_ussd_message()
        status = self.send_ussd("Please Confirm", "1", "airtime")

        if not status:
            print("Failed to send confirmatin for Safaricom Airtime", flush=True)
            return
        #invalid pfone safaricom phone No
        message_text = self.get_ussd_message()
        status = self.send_ussd("(Ex: 07xxxxxxxx)", "*", "airtime")
        
        if not status:
            print("Detecting Invalid phone number is  failed", flush=True)
            self.update_status("Airtime topup", [16], "Fail", 7)
        else:
            print(f"Detecting Invalid phone number is pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [16], "Pass", 7)

        # Enter valid phone number
        phone_sf = self.safaricom_number
        print(f"Entering phone number {phone_sf}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_sf , "Safaricom Airtime")

        if not status:
            print("Failed to send phone for Safaricom Airtime", flush=True)
            return
        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Safaricom Airtime")

        if not status:
            print("Failed to send amount for Safaricom Airtime", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "airtime")

        if not status:
            print("airtime confirmation failed", flush=True)
            self.update_status("Airtime topup", [12], "Fail", 7)
        else:
            print(f"airtime confirmation pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [12], "Pass", 7)
            time.sleep(0.5)


        print("Airtime transaction completed", flush=True)
        self.cancel_ussd()