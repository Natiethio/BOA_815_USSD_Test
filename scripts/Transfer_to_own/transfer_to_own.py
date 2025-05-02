import unittest
import time
import re
import sys
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
from Helpers.transfer_to_own_helper import transfer_to_own_helper


def transfer_to_own_account(self):
        try:
            # self.enter_pin_to_login()


            status_helper = transfer_to_own_helper(self)

            time.sleep(0.5)
            print("Test for Transfer to Own ..", flush=True)


            if not status_helper:
                print("No home page found retrying")
                # self.cancel_ussd()

                retries = 3

                for _ in range(retries):
                    status_helper = transfer_to_own_helper(self)
                    if status_helper:
                        break
                    else:
                     print("Home page not matched retrying...", flush=True)
                
                if not status_helper:
                    print("Failed after retries",flush=True)
                    print("No home page found retrying",flush=True)
                    self.cancel_ussd()
                    return
            

            # Step 1: Select debit account
            message = self.get_ussd_message()
            if "transfer to own" not in message.lower():
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
            # Get available accounts
            accounts = [line for line in message.split("\n") if "ETB" in line or "Dollar" in line]
            if not accounts:
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
            # Select first account as debit account
            debit_account_option = accounts[0].split(":")[0].strip()
            self.send_ussd_input(debit_account_option)
            
            # Step 2: Select credit account (should show other accounts)
            message = self.get_ussd_message()
            if "Funds Transfer Own Account" not in message:
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
            # Verify the debit account is not in the list
            accounts = [line for line in message.split("\n") if "ETB" in line or "Dollar" in line]
            if not accounts:
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
            # Select first available account as credit account
            credit_account_option = accounts[0].split(":")[0].strip()
            self.send_ussd_input(credit_account_option)
            
            # Step 3: Enter amount
            message = self.get_ussd_message()
            if "Request Debit" not in message:
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
            # Test with amount that exceeds normal limits (should still work for own account transfer)
            large_amount = "1000000"  # 1,000,000 ETB

            self.send_ussd_input(1)
            message = self.get_ussd_message()

            
            self.send_ussd_input(self.amount)
            
            # Step 4: Enter remark
            message = self.get_ussd_message()
            # if "A space will be provided to upload remark" not in message:
            #     self.update_status("Transfer", [72], "Fail", 7)
            #     return False

            self.send_ussd_input(1)
            message = self.get_ussd_message()
                
            self.send_ussd_input("testremark")
            
            # Step 5: Confirm transfer
            message = self.get_ussd_message()
            # if "A confirmation notification will be displayed" not in message:
            #     self.update_status("Transfer", [72], "Fail", 7)
            #     return False
                
            self.send_ussd_input("1")  # Confirm
            
            # Verify success
            message = self.get_ussd_message()
            if "complete" in message.lower() or "debited" in message.lower():
                print("Transfer to own account successful", flush=True)
                self.update_status("Transfer", [72], "Pass", 7)
                return True
            else:
                self.update_status("Transfer", [72], "Fail", 7)
                return False
                
        except Exception as e:
            print(f"Error in transfer_to_own_account: {e}", flush=True)
            self.update_status("Transfer", [72], "Fail", 7)
            return False