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


def instant_transfer(self):

    self.enter_pin_to_login()

    print("Test for Instant Transfer..", flush=True)
  
    for _ in range(3):
            status_helper = otherbank_helper(self)
            if status_helper:
                print("Home page matched", flush=True)
                break
            print("Home page not matched, retrying...", flush=True)
    else:
                print("Failed to land on home page after retries continuing..", flush=True)
                self.cancel_ussd()
                return

    print("Test for Positive Instant Transfer Scenario for Other Bank Transfer Started", flush=True)

    result = handle_transfer(self, self.amount, is_negative=False)

        # if result != "success":
        #     return

    if result != "success":
        print("Positive test failed after retries. exiting ...", flush=True)
        self.cancel_ussd()
        return
    
    self.send_ussd_input("*")

    print("Test for Positive Scenario for Instant Transfer Finished Test for Negative Scenario Begines...", flush=True)


    WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
    )

    otherbank_helper(self)

    handle_transfer(self, "50000", is_negative=True, scenario_type="daily")

    handle_transfer(self, "50100", is_negative=True, scenario_type="single", skip_initial_steps=True)

    print("Test for Transfer to Other Banks(Instant Transfer) Compleated", flush=True)

    print_and_clear_slow_popups(self, "Transfer to Other Banks(Instant)")

    self.cancel_ussd()
    

def handle_transfer(self, amount, is_negative, scenario_type=None, skip_initial_steps=False):
    retries = 3
    attempt = 0

    bank = self.bank_name

    bank_account = self.bank_account

    if not skip_initial_steps:
            
            expected_ResultB = [
              "Transfer to Other Bank",
              "1: Instant Transfer",
              "2: Non Instant Transfer"
            ]

            
            if not self.send_ussd( expected_ResultB, "1", "Transfer_to_Other_Bank", "Other Bank List Page"):
                    print("No bank list of transfer options found", flush=True)
                    self.update_status("Transfer", [48], "Fail", 5, screenshot_name="no_transfer_options_found")
                    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_transfer_options_found")
                    return "fail"
            else :
                 print("List of transfer to other bank option found", flush=True)
                 self.update_status("Transfer", [48], "Pass", 5)

            if not self.send_ussd(["Bank"], bank, "Transfer_to_Other_Bank", "Enter Account Page(Other Bank Transfer)"):
                    print("No bank list found terminating transfer to other bank operation", flush=True)
                    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_bank_list_found")
                    return "fail"
            
            if not is_negative:
            
                    print("Testing Invalid Account", flush=True)
                    
                    if not self.send_ussd("Enter Account", "10101010101100", "Transfer_to_Other_Bank", "BOA Account List Page(Instant Transfer)"):
                            print("No account entry page found, exiting", flush=True)
                            self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_account_entry_page_found")
                            return "fail"
                    
                    if not self.send_ussd("Account doesn't exist.", "*", "Transfer_to_Other_Bank", "Enter Account Page(Other Bank Transfer)"):
                            print("Account validation failed exiting..", flush=True)
                            self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_invalid_account_validation")
                            self.update_status("Transfer", [52], "Faild to validate invalid account", 6)
                            return "fail"
                    
                    if not self.send_ussd(["Bank"], bank, "Transfer_to_Other_Bank", "Enter Account Page(Other Bank Transfer)"):
                        print("No bank list found terminating transfer to other bank operation", flush=True)
                        self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_bank_list_found")
                        return "fail"
                    
                    print("Testing Invalid Account Passed", flush=True)
            

            for i in range(3):
                print(f"Attempt {i + 1} to enter valid account number...", flush=True)

                if not self.send_ussd("Enter Account", bank_account, "Transfer_to_Other_Bank", "BOA Account List Page(Instant Transfer)"):
                    print("No account entry page found, exiting", flush=True)
                    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_account_entry_page_found")
                    return "fail"

                response_text = self.get_ussd_message()

                if "instant transfer" in response_text.lower():
                    print("Account accepted successfully", flush=True)
                    break 

                else:
                    print("Account not accepted, retrying...", flush=True)
                    self.send_ussd_input("*")  
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                    )
                    if not self.send_ussd(["Bank"], bank, "Transfer_to_Other_Bank", "Enter Account Page(Other Bank Transfer Retry)"):
                        print("Bank list not found during retry", flush=True)
                        self.update_status("Transfer", [52], "Fail", 5, screenshot_name="bank_list_missing_on_retry")
                        return "fail"
            else:
                print("All account entry attempts failed proceading to next test failed for Transfer to other bank operation", flush=True)
                self.update_status("Transfer", [52], "Fail", 5, screenshot_name="account_not_accepted_after_retries")
                for _ in range(2):
                    self.send_ussd_input("*")
                
                return "fail"
                        

            txn_text = self.get_ussd_message()
            account_option, detected_account = extract_staff_or_saving_option(self, txn_text)

            if not account_option or bank_account == detected_account:
                print("Error: Source and destination accounts can not be the same. Retrying...", flush=True)
                return "fail"

            if not self.send_ussd(["Instant Transfer"], account_option, "Transfer_to_Other_Bank", "Enter Amount Page(Instant)"):
                    print("Error: No Account list found", flush=True)
                    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_act_list_found")
                    return "fail"

    while attempt < retries:
        try:
            if attempt > 0:
                print(f"Trying transfer attempt {attempt + 1} for amount {amount}...", flush=True)


            if not self.send_ussd(["Enter Amount"], amount, "Transfer_to_Other_Bank", "Confirmation Page(Instant)"):
                print("No account Entery page found exiting .. ", flush=True)
                self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_act_entery_page_found")
                return "fail"


            if not self.send_ussd(["Please Confirm"], "1", "Transfer_to_Other_Bank", "Success Screen Page(Instant Transfer)"):
                print("No confirmation page found .. ", flush=True)
                self.update_status("Transfer", [52], "Fail", 5, screenshot_name="no_act_entery_page_found")
                return "fail"


            # if not self.send_ussd(["Complete"], "1", "Transfer_to_Other_Bank"):
            #     raise Exception("Transfer not completed")
            

            final_text = self.get_ussd_message()
            time.sleep(2)
            print(f"USSD response:\n{final_text}", flush=True)

            if "exceeded the daily transaction limit for instant transfer" in final_text.lower():
                if is_negative and scenario_type == "daily":
                    print("Daily Limit Negaive Scenario Passed", flush=True)
                    self.update_status("Transfer", [57], "Pass", 5)
                    self.send_ussd_input("*")
                    return "success"
                else:
                    print("Daily Limit Negaive Scenario Failed", flush=True)
                    self.update_status("Transfer", [55, 57], "Fail", 5, screenshot_name="daily_limit_bypass")
                    return "fail"

            elif "exceeded the single transaction limit for instant transfer" in final_text.lower():
                if is_negative and scenario_type == "single":
                    self.update_status("Transfer", [55,56], "Pass", 5)
                    print("Single Limit Negaive Scenario Passed", flush=True)
                    self.send_ussd_input("*")
                    return "success"
                else:
                    print("Single Limit Negaive Scenario Failed", flush=True)
                    self.update_status("Transfer", [55, 56], "Fail", 5, screenshot_name="single_limit_bypass")
                    return "fail"

            elif any(err in final_text for err in ["repository.productTransaction", "productTransactionAlreadyExists", "ORA-12899", "value too large for column"]):
                print("Recoverable error detected. Retrying from amount entry...", flush=True)
                self.send_ussd_input("*")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                )
                attempt += 1
                continue

            elif "complete" in final_text.lower() or "debited" in final_text.lower():
                if not is_negative:
                    print("Transfer Successfuly")
                    self.update_status("Transfer", [52], "Pass", 5)
                    # self.send_ussd_input("*")
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                    )
                    # otherbank_helper(self)
                    return "success"
                else:
                    print("Unexpected success in negative test", flush=True)
                    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="retry_exhausted")
                    return "fail"

            else:
                print("Unexpected final text, retrying...", flush=True)
                self.send_ussd_input("*")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                )
                attempt += 1

        except Exception as e:
            print(f"Exception occurred during transfer attempt {attempt + 1}: {str(e)}", flush=True)
            self.send_ussd_input("*")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
            )
            attempt += 1

    print("Retries exhausted. Returning to home.", flush=True)

    for _ in range(4):
        self.send_ussd_input("*")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
        )
    self.update_status("Transfer", [52], "Fail", 5, screenshot_name="retry_exhausted")
    otherbank_helper(self)
    return "fail"

def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()