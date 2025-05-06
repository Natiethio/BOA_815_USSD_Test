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
from Helpers.enter_account_and_select_valid_option import enter_account_and_select_valid_option

def transfer_within_BOA(self):
        
        self.enter_pin_to_login()


        status_helper = transfer_helper(self)

        time.sleep(5)
        print("Test for Transfer withen BOA ..", flush=True)


        if not status_helper:
            print("No home page found retrying")
            # self.cancel_ussd()

            retries = 3

            for _ in range(retries):
                status_helper = transfer_helper(self)
                if status_helper:
                    break
                else:
                  print("Home page not matched retrying...", flush=True)
            
            if not status_helper:
                print("Failed after retries",flush=True)
                print("No home page found retrying",flush=True)
                self.cancel_ussd()
                return

        # if not transfer_helper(self):
        #     print("Initial transfer helper failed.", flush=True)
        #     # return

        # print("Test for Transfer within BoA", flush=True)


        expected_ResultB = [
            "Transfer",
            "1: Transfer within BoA", 
            "2: ATM withdrawal",
            "3: Load to TeleBirr",
            "4: Transfer to M-PESA",
            "5: Awach"
        ]
        
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
        )

        status = self.send_ussd(expected_ResultB, "1", "transfer_with_boa", "Enter Account Page")

        if not status:
            self.update_status("Transfer", [2], "Fail", 5, screenshot_name="no_transferhomepage")
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)

        self.update_status("Transfer", [2], "Pass", 5)


        if not enter_account_and_select_valid_option(self): #not handeld
            self.cancel_ussd()
            return
            

        print("Executing first round with user-input amount...", flush=True)

        if not handle_transfer_flow(self, is_negative_scenario=False, predefined_amount=self.amount, exceeded_amount=""):
            print("failed on first handel user input transfer call",flush=True)
            return
        
        self.send_ussd_input("*")
        time.sleep(1)

        fixed_amounts = [500000, 502000]  


        for idx, test_amt in enumerate(fixed_amounts, start=2): 
                print(f"Testing Negative Scenario Round {idx} with amount: {test_amt}", flush=True)

               
                if idx == 2:
                    if not transfer_helper(self):
                        print("Retrying transfer helper failed...", flush=True)
                        return

                    status = self.send_ussd(expected_ResultB, "1", "transfer_with_boa", "Enter Amount Page")
                    if not status:
                        return

                    if not enter_account_and_select_valid_option(self):
                        return

                result = handle_transfer_flow(
                    self,
                    is_negative_scenario=True, 
                    predefined_amount="", 
                    exceeded_amount=test_amt, 
                    round_idx=idx  
                )

                if result == "retry":
                    print("Retrying the same round due to duplicate transaction error.", flush=True)
                    if not self.send_ussd_input("*"):
                        print("Failed to navigate back after duplicate transaction error", flush=True)
                    continue  

                if not result:
                    return 
        
        time.sleep(0.5)

        print("Transfer with BOA complated",flush=True)

        time.sleep(0.5)
        print_and_clear_slow_popups(self, "Transfer Within BOA")
        self.cancel_ussd()
        return True


def handle_transfer_flow(self, is_negative_scenario, predefined_amount, exceeded_amount, round_idx=0):
            amount = predefined_amount if not is_negative_scenario else exceeded_amount

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
            )

            print(f"Entering amount: {amount}", flush=True)
            if not self.send_ussd(["Enter Amount"], amount, "transfer_with_boa", "Enter Remark Page"):
                print("Amount entry failed", flush=True)
                return False

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
            )
            print("Entering remark: testremark", flush=True)
            if not self.send_ussd(["Enter Remark"], "testremark", "transfer_with_boa", "Transfer Confirmation Page"):
                print("Remark entry failed", flush=True)
                return False

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
            )
            confirm_text = self.get_ussd_message()
            print(f"Confirmation screen:\n{confirm_text}", flush=True)

            if not self.send_ussd(["Please Confirm"], "1", "transfer_with_boa", "Sucess Screen"):
                print("Confirmation failed", flush=True)
                return False

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
            )
            final_text = self.get_ussd_message()
            print(f"Final response:\n{final_text}", flush=True)

            self.last_response = final_text  

           
            if "exceeded the daily transaction limit" in final_text.lower():
                print("Transfer failed due to daily limit  error.", flush=True)
                if is_negative_scenario:
                    self.update_status("Transfer", [8], "Pass", 5)
                    self.send_ussd_input("*")  
                    return True
                else:
                    self.update_status("Transfer", [8], "Fail", 5, screenshot_name="dailylimitbypass")
                    return False

            if "exceeded the single transaction limit" in final_text.lower():
                print("Transfer failed due to single limit.", flush=True)
                if is_negative_scenario:
                    self.update_status("Transfer", [9], "Pass", 5)
                    self.send_ussd_input("*")  
                    # self.cancel_ussd()
                    return True
                else:
                    self.update_status("Transfer", [9], "Fail", 5, screenshot_name="singletraslimitbypass")
                    return False

            
            if "repository.productTransaction" in final_text or "productTransactionAlreadyExists" in final_text:
                print("Duplicate transaction or repo error. Will retry after going back.", flush=True)
                # self.send_ussd_input("*")
                return "retry"

            
            if "complete" in final_text.lower() or "debited" in final_text.lower():
                print("Transfer successfully", flush=True)
                self.update_status("Transfer", [5], "Pass", 5)
                return True

            print("Transfer response could not be validated.", flush=True)
            return False


def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()