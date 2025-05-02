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
from Helpers.transfer_helper import transfer_helper
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option

def enter_account_and_select_valid_option(self):
            expected_prompt = ["Enter Account No"]
            
            for attempt in range(1, 4):
                time.sleep(0.5)
                accountno = self.account_number 
                print(f"Attempt {attempt}: Entering account number {accountno}", flush=True)

                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                )
                
                status = self.send_ussd(expected_prompt, accountno, "transfer_with_boa", "BOA Account List Page")

                if not status:
                    print("Account number entry failed.", flush=True)
                    return False
                
               
                txn_text = self.get_ussd_message()
                print(f"USSD message after entering account:\n{txn_text}", flush=True)


                account_option, detected_account = extract_staff_or_saving_option(self, txn_text)

                if not account_option or not detected_account:
                    print("No valid STAFF or SAVING account detected. Retrying...", flush=True)
                    self.send_ussd_input("*")  
                    continue
                
                #not handeld
                if accountno == detected_account: # not handeld
                    print("Error: Source and destination accounts are the same. Retrying...", flush=True)
                    self.send_ussd_input("*")
                    if attempt == 3:
                        self.cancel_ussd()
                        return False
                    continue

                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                )
                
                self.send_ussd(["Transfer within BoA"], account_option, "transfer_with_boa", "Amount Entery Page")
                return True

            print("Failed to enter a valid account after 3 attempts.", flush=True)
            return False