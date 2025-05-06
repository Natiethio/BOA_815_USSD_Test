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
from Helpers.otherbank_helper import otherbank_helper
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option

def non_instant_transfer(self):

        self.enter_pin_to_login()

        print("Test for Non-Instant Transfer..", flush=True)
        
        for _ in range(3):
            status_helper = otherbank_helper(self)
            if status_helper:
                print("Transfer to other bank's Home page matched", flush=True)
                break
            print("Home page not matched, retrying...", flush=True)
        else:
                print("Failed to land on home page after retries continuing..", flush=True)
                self.cancel_ussd()
                return

        print("Test for Negative Non Instant Transfer Scenario for Other Bank Transfer Started", flush=True)


        result = handle_transfer(self, 200100, is_negative=True, skip_initial_steps=False)

        if result != "success":
           print("Negative test failed or partially completed, continuing...", flush=True)
    
        print("Negative Test Completed. Starting Positive Test for Non-Instant Transfer...", flush=True)

        result = handle_transfer(self, self.amount, is_negative=False, skip_initial_steps=True)

        if result != "success":
           print("Positive test failed for non instant transfer", flush=True)

        print("Test for Transfer to Other Banks(Non-Instant Transfer) Compleated", flush=True)

        print_and_clear_slow_popups(self, "Transfer to Other Banks(Non Instant)")

        self.cancel_ussd()


def handle_transfer(self, amount, is_negative, skip_initial_steps=False,  retries=3):
    attempt = 0
    bank_account = self.bank_account
    skip_to_confirm = not is_negative


    expected_ResultB = [
        "Transfer to Other Bank",
        "1: Instant Transfer",
        "2: Non Instant Transfer"
        ]
    
    if not skip_initial_steps:
                  
                if not self.send_ussd(expected_ResultB, "2", "Transfer_to_Other_Bank", "BOA Account Lists Page(Non Instant)"):
                        print("No List of transfer options found exiting fot Non instant Transfer..", flush=True)
                        self.update_status("Transfer", [48, 62], "Fail", 5, screenshot_name="no_transfer_options_found")
                        self.cancel_ussd()
                        return "fail"
                else :
                        print("List of transfer to other bank option found", flush=True)
                        self.update_status("Transfer", [48], "Pass", 5)

                print("Selecting Account..")
                txn_text = self.get_ussd_message()
                account_option, detected_account = extract_staff_or_saving_option(self, txn_text)

                if not account_option or bank_account == detected_account:
                        print("Source and destination accounts can't be the same.", flush=True)
                        return "fail"

                if not self.send_ussd(["Non Instant Transfer"], account_option, "Transfer_to_Other_Bank", "Enter Name Page"):
                        print("Error: No BOA Account list found", flush=True)
                        self.update_status("Transfer", [62,48], "Fail", 5, screenshot_name="no_act_list_found")
                        return "fail"

    while attempt < retries:
        print(f"Attempt {attempt + 1}: Starting Transfer Flow", flush=True)
        
        print("Entering Name..", flush=True)
        if not self.send_ussd(["Enter Name"], self.name, "Transfer_to_Other_Bank", "Bank's List Page"):
                print("Error: No name entery page found", flush=True)
                self.update_status("Transfer", [62,48], "Fail", 5, screenshot_name="no_name_entery_page")            
                return "fail"

        expected_ResultC = [
           "Request Non Instant Transfer",
           "Bank" ]
                            
        print("Selecting Bank", flush=True)
        if not self.send_ussd(expected_ResultC, self.bank_name, "Transfer_to_Other_Bank", "Enter Account Page"):
                print("No bank list found terminating transfer to other bank(Non Instant) operation", flush=True)
                self.update_status("Transfer", [62], "Fail", 5, screenshot_name="no_bank_list_found")
                return "fail"

        print("Entering Account Number", flush=True)
        if not self.send_ussd(["Enter Account"], self.bank_account, "Transfer_to_Other_Bank", "Enter Amount Page"):
                print("No account entry page found, exiting", flush=True)
                self.update_status("Transfer", [62], "Fail", 5, screenshot_name="no_account_entery_pagefound")
                return "fail"

        print("Entering Amount", flush=True)           
        if not self.send_ussd(["Enter Amount"], amount, "Transfer_to_Other_Bank", "Confirmation Page"):
                print("No amount entry page found, exiting", flush=True)
                self.update_status("Transfer", [62], "Fail", 5, screenshot_name="no_amount_entery_pagefound")
                return "fail"
        
        txn_text = self.get_ussd_message()

        if skip_to_confirm:
                expected = "Please Confirm"
                if expected.lower() not in txn_text.lower():
                        print(f"Expected text not found: '{expected}'", flush=True)
                        self.update_status("Transfer", [62], "Fail", 5, screenshot_name="no_confirmation_pagefound")
                        return "fail"
                else:
                        print("Positive scenario: reached confirmation page. Navigating back and ending test (Non Instant Transfer).", flush=True)
                        self.update_status("Transfer", [62], "Pass", 5)
                        self.send_ussd_input("*")
                        return "success"
                
        
        print("Confirming..", flush=True)
        confirm_result = self.send_ussd(["Please Confirm"], "1", "Transfer_to_Other_Bank", "Single limit exceeded page")

        if confirm_result:
            msg = self.get_ussd_message()
            if "exceeded the single transaction limit" in msg.lower():
                print("Single Limit Negaive Scenario Passed", flush=True)
                self.update_status("Transfer", [66], "Pass", 5)
                self.send_ussd_input("*")  
                return "success"
            
            else:
                msg = self.get_ussd_message()
                if any(err in msg for err in [
                        "repository.productTransactionAlreadyExists",
                        "ORA", "value too large for column"
                ]):
                        print("Recoverable error occurred: retrying current flow...", flush=True)
                        self.send_ussd_input("*")  
                        attempt += 1
                        continue


    if attempt == retries:
        print("Failed negative scenario limit error after retries.", flush=True)
        self.update_status("Transfer", [66], "Fail", 5, screenshot_name="failed_after_retries")
        return "fail"

    return "success"


def print_and_clear_slow_popups(self, func_name):
                    if self.slow_popups:
                        
                        print(f"\n[Slow Popups in {func_name}]")
                        for page, duration in self.slow_popups:
                            print(f"{page}: {duration}s")
                        self.slow_popups.clear()   


                                


