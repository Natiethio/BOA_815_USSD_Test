import unittest
import time
import re
import sys
import os
from Helpers.airtime_helper import airtime_helper
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option

def airtime(self):

  ethiotelecom = airtime_topup_for_ethio_telecom(self)
    
  safaricom = airtime_topup_for_safaricom(self)

  print_and_clear_slow_popups(self, "Air Time TopUp")


  #testing for airtime topup for safaricom


def airtime_topup_for_ethio_telecom(self):
    print("Test for Ethio telecom topup")
    print(self.pin)
    print(self.etl_number)

    self.enter_pin_to_login()

    if not airtime_helper(self):
        print("No home page found")
        return

    print("Test for Airtime EthioTelecom..", flush=True)

    expected_menu = [
        "Airtime",
        "1: EthioTelecom Airtime",
        "2: Safaricom Airtime",
    ]
    if not self.send_ussd(expected_menu, "1", "EthioTelecom Airtime", "BOA Accounts list Page(Air Time)"):
        self.update_status("Airtime topup", [2], "Fail", 5)
        return
    self.update_status("Airtime topup", [2], "Pass", 5)

    message_text = self.get_ussd_message()
    account_option, account_number = extract_staff_or_saving_option(self, message_text)
    if not account_option:
        print("No valid STAFF or SAVING account found", flush=True)
        self.cancel_ussd()
        return

    print(f"Processing account: {account_number}", flush=True)
    if not self.send_ussd("EthioTelecom Airtime", account_option, "EthioTelecom Airtime", "Enter Recharge Phone No Page(Ethio Telecom)"):
        print("Failed to select account", flush=True)
        return
    
    # Invalid Phone Test
    invalid_phone = "0712911008"
    print(f"Test for invalid ethio telecom phone number: {invalid_phone}", flush=True)

    status = self.send_ussd("Enter Recharge Phone No", invalid_phone, "EthioTelecom Airtime", "Enter Amount(Air Time)")
    if not status:
        print("Failed to enter invalid phone number", flush=True)
        return

    status = self.send_ussd("Enter Amount", self.amount, "EthioTelecom Airtime", "Confirmation Page(Air Time)")
    if not status:
        print("Failed to enter amount for invalid phone", flush=True)
        return

    status = self.send_ussd("Please Confirm", "1", "airtime", "Invalid Ethio Telecom Phone No page")

    if not status:
        print("Failed to confirm transaction for invalid phone", flush=True)
        return

    response = self.get_ussd_message()
    

    status = self.send_ussd("(Ex: 09xxxxxxxx)", "*", "airtime", "Enter Valid Recharge Phone No Page(Ethio Telecom)")

    if not status:
        print("Detecting Invalid ethio telecom phone number validation is  failed checking possible condtions..", flush=True)
        # self.update_status("Airtime topup", [9], "Pass", 5)
        # self.send_ussd("(Ex: 09xxxxxxxx)", "*", "airtime")

        if "repository.productTransaction" in response or "productTransactionAlreadyExists" in response or "value too large for column" in response:
      
            max_retries = 3
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                    print(f"Attempt {retry_count + 1} for valid EthioTelecom top-up", flush=True)

                    response = self.get_ussd_message()

                    print(f"Recoverable error encountered: {response}", flush=True)
                    self.send_ussd("productTransactionAlreadyExists", "*", "airtime", "Enter Recharge Phone No Page(Ethio Telecom Retry)")

                    status = self.send_ussd("Enter Recharge Phone No", invalid_phone, "EthioTelecom Airtime", "Enter Amount Page(Air Time)")

                    if not status:
                        print("Failed to enter phone number", flush=True)
                        return

                    status = self.send_ussd("Enter Amount", self.amount, "EthioTelecom Airtime", "Confirmation Page(Air Time)")
                    if not status:
                        print("Failed to enter amount for invalid phone", flush=True)
                        return

                    status = self.send_ussd("Please Confirm", "1", "airtime", "Invalid Phone Page")

                    if not status:
                        print("Failed to confirm transaction for invalid phone", flush=True)
                        return
                    
                    response = self.get_ussd_message()

                    if "(Ex: 09xxxxxxxx)" in response:
                        print("Detected invalid phone number correctly", flush=True)
                        self.update_status("Airtime topup", [9], "Pass", 5)
                        self.send_ussd("(Ex: 09xxxxxxxx)", "*", "airtime", "Enter Recharge Phone No Page(Ethio Telecom)")
                        success = True
                        break
                    else:
                        print("Failed to detect invalid phone number", flush=True)
                        # self.update_status("Airtime topup", [9], "Fail", 5)
                        self.send_ussd_input("*")
                        continue

            if not success:
                print("Final airtime top-up invalid phonr test failed after retries", flush=True)
                self.update_status("Airtime topup", [9], "Fail", 5)
        

        else:
            print("Failed to detect invalid ethio telecom phone number", flush=True)
            self.update_status("Airtime topup", [9], "Fail", 5)

    else:
        print(f"Detecting invalid ethio telecom phone number is pass for: {account_number}", flush=True)
        self.update_status("Airtime topup", [16], "Pass", 5)

    phone_et = self.etl_number
    print(f"Test for valid ethio telecom phone number: {phone_et}", flush=True)

    status = self.send_ussd("Enter Recharge Phone No", phone_et , "EthioTelecom Airtime", "Enter Amount Page(Air Time)")

    if not status:
        print("Failed to send phone for EthioTelecom Airtime", flush=True)
        return

    amount = self.amount
    status = self.send_ussd("Enter Amount", amount, "EthioTelecom Airtime", "Confirmation Page(Air Time)")

    if not status:
        print("Failed to send amount for EthioTelecom Airtime", flush=True)
        return
        
    # Confirm transaction
    message_text = self.get_ussd_message()

    status = self.send_ussd("Please Confirm", "*", "airtime","Enter Amount(Air Time Back)")

    if not status:
        print("airtime confirmation failed", flush=True)
        self.update_status("Airtime topup", [5], "Fail", 5)

    else:
        print(f"airtime confirmation pass for {account_number}", flush=True)
        self.update_status("Airtime topup", [5], "Pass", 5)
        time.sleep(0.5)


    print("Ethio Telecom Airtime Top up Test completed!", flush=True)
    self.cancel_ussd()
    # return True


def airtime_topup_for_safaricom(self):
        print("Test for safaricom topup")
        print(self.pin)
        print(self.safaricom_number)

        self.enter_pin_to_login()

        status_helper = airtime_helper(self)

        time.sleep(5)
        print("Test for Airtime Safaricom ..", flush=True)

        # status_helper = self.airtime_helper()

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            # airtime_topup_for_safaricom(self)
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

        status = self.send_ussd(expected_ResultB ,"2","Safaricom Airtime", "BoA Accounts List Page(Air Time)")

        if not status:
            self.update_status("Airtime topup", [2], "Fail", 5)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
            return

        self.update_status("Airtime topup", [2], "Pass", 5)

        message_text = self.get_ussd_message()

        # Extract STAFF or SAVING account options
        account_option, account_number = extract_staff_or_saving_option(self, message_text)
        
        if not account_option or not account_number:
            print("No valid STAFF or SAVING account found", flush=True)
            self.cancel_ussd()
            return

        print(f"Processing account: {account_number}", flush=True)
        
        # Select the account
        status = self.send_ussd("Safaricom Airtime", account_option, "Safaricom Airtime" , "Enter Recharge Phone No(Safaricom)")

        if not status:
            print("Failed to select account", flush=True)
            return

        # Enter phone invalid number 
        phone_saf_inv = "0970951608"
        print(f"Test for invalid safaricom phone number validation: {phone_saf_inv}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_saf_inv , "Safaricom Airtime" ,"Enter Amount(Air Time Safaricom)")

        if not status:
            print("Failed to send phone for Safaricom Airtime", flush=True)
            return

        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Safaricom Airtime", "Confirmation Page(Air Time Safaricom)")

        if not status:
            print("Failed to send amount for Safaricom Airtime", flush=True)
            return

        # Confirm transaction
        # message_text = self.get_ussd_message()
        status = self.send_ussd("Please Confirm", "1", "airtime", "Invalid Safaricom Number Page")

        if not status:
            print("Failed to send confirmatin for Safaricom Airtime", flush=True)
            return
        
        #invalid pfone safaricom phone No
        message_text = self.get_ussd_message()
        status = self.send_ussd("(Ex: 07xxxxxxxx)", "*", "airtime", "Enter Recharge Phone No(Safaricom)")
        
        if not status:
            print("Detecting Invalid safaricom phone number is failed checking possible condtions..", flush=True)
            # self.update_status("Airtime topup", [16], "Fail", 5)
             
            if "repository.productTransaction" in response or "productTransactionAlreadyExists" in response or "value too large for column" in response:
      
              max_retries = 3
              retry_count = 0
              success = False

              while retry_count < max_retries and not success:
                    print(f"Attempt {retry_count + 1} for valid Safaricom top-up", flush=True)

                    response = self.get_ussd_message()

                    print(f"Recoverable error encountered: {response}", flush=True)
                    self.send_ussd("productTransactionAlreadyExists", "*", "airtime", "Enter Recharge Phone No(Safaricom)")

                    status = self.send_ussd("Enter Recharge Phone No", phone_saf_inv, "EthioTelecom Airtime", "Enter Amount Page(Air Time)")

                    if not status:
                        print("Failed to enter phone number", flush=True)
                        return

                    status = self.send_ussd("Enter Amount", self.amount, "EthioTelecom Airtime", "Confirmation Page(Air Time)")
                    if not status:
                        print("Failed to enter amount for invalid phone", flush=True)
                        return

                    status = self.send_ussd("Please Confirm", "1", "airtime", "Invalid Safaricom Number Page")

                    if not status:
                        print("Failed to confirm transaction for invalid phone", flush=True)
                        return
                    
                    response = self.get_ussd_message()

                    if "(Ex: 09xxxxxxxx)" in response:
                        print("Detected invalid phone number correctly", flush=True)
                        self.update_status("Airtime topup", [16], "Pass", 5)
                        self.send_ussd("(Ex: 09xxxxxxxx)", "*", "airtime", "Enter Recharge Phone No(Safaricom)")
                        success = True
                        break
                    else:
                        print("Failed to detect invalid safaricom phone number", flush=True)
                        self.update_status("Airtime topup", [16], "Fail", 5)
                        self.send_ussd_input("*")
                        break

              if not success:
                    print("Final airtime top-up invalid phonr test failed after retries", flush=True)
                    self.update_status("Airtime topup", [16], "Fail", 5)
           
            else:
                print("Failed to detect invalid safaricom phone number", flush=True)
                self.update_status("Airtime topup", [16], "Fail", 5)

        else:
            print(f"Detecting Invalid phone number safaricom is pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [16], "Pass", 5)

        # Enter valid phone number
        phone_sf = self.safaricom_number
        print(f"Tesf for valid safaricom phone number: {phone_sf}", flush=True)

        status = self.send_ussd("Enter Recharge Phone No", phone_sf , "Safaricom Airtime", "Enter Amount(Air Time)")

        if not status:
            print("Failed to send phone for Safaricom Airtime", flush=True)
            return
        # Enter amount
        amount = self.amount
        status = self.send_ussd("Enter Amount", amount, "Safaricom Airtime", "Confirmation Page(Air Time)")

        if not status:
            print("Failed to send amount for Safaricom Airtime", flush=True)
            return
        
        # Confirm transaction
        message_text = self.get_ussd_message()

        status = self.send_ussd("Please Confirm", "*", "airtime","Enter Amount(Air Time Back)")

        if not status:
            print("airtime confirmation failed", flush=True)
            self.update_status("Airtime topup", [12], "Fail", 5)
        else:
            print(f"airtime confirmation pass for {account_number}", flush=True)
            self.update_status("Airtime topup", [12], "Pass", 5)
            time.sleep(0.5)


        print("Safaricom Airtime Top Up Test transaction completed!", flush=True)
        self.cancel_ussd()

def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()