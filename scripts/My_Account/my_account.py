
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


def my_account(self):
            try:

                input_field = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.android.phone:id/input_field']"))
                )
                input_field.clear()

                expected_result = [
                    "Welcome to BOA Mobile Banking",
                    "1: My Accounts"
                ]

                if not self.send_ussd(expected_result, "1", "My_Accounts", "My BOA Accounts Lists Page"):
                    print("No Home page found Exiting", flush=True)
                    return


                message_text = self.get_ussd_message()

                print("USSD Response:", message_text, flush=True)

                assert "My Accounts" in message_text , "Did not land on the expected 'My Accounts' page"

                accounts = [line for line in message_text.split("\n") if "ETB" in line or "Dollar" in line]
                print(accounts, flush=True)

                if not accounts:
                  self.update_status("Accounts", [2], "Fail", 5, screenshot_name="my_accounts_noaccountsfound")
                  self.fail("No ETB or Dollar accounts found.")
                else:
                  print("list of accounts associated with the customer ID is displayed", flush=True)
                  self.update_status("Accounts", [2], "Pass", 5) #pass
        
                  print("Excel status Updated", flush=True)
                print(f"{len(accounts)} account(s) found: {accounts}", flush=True)

                for i, acc in enumerate(accounts, start=1):
                    print(f"\nChecking Account {i}: {acc}", flush=True)

                    print(acc.split("-")[0].strip(), flush=True)

                    account_number_acc = acc.split(":")[1].split("-")[0].strip()

                    print(account_number_acc, flush=True)

                    expected_resultB = [
                        "My Accounts"
                        ]


                    if not self.send_ussd(expected_resultB, str(i), "My_Accounts", "Transactions List Page"):
                        print("No Account list found terminating my account operation", flush=True)
                        # self.update_status("Accounts", [2], "Pass", 5, screenshot_name="no_bank_list_found")
                        return
                    
                    expected_resultC = [
                        account_number_acc,
                        "Cleared Balance",
                        "Transactions"
                    ]

                    if not self.send_ussd(expected_resultC, "1", "My_Accounts", "Transaction Detail Page"):
                        print("No List of transaction displayed", flush=True)
                        self.update_status("Accounts", [4], "Fail", 5, screenshot_name="no_resent_trs_list_found")
                    
                    else:
                        print("The list of recent transactions is displayed", flush=True)
                        self.update_status("Accounts", [4], "Pass", 5)
                    

                    expected_resultD = [
                        account_number_acc,
                        "ETB",
                        "Press any key for more"
                    ]

                    if not self.send_ussd(expected_resultD, "*", "My_Accounts"):
                        print("No List of transaction displayed", flush=True)
                        print("Transaction detail page can't be verified", flush=True)
                        self.update_status("Accounts", [6], "Fail", 5, screenshot_name="my_accounts_notransactiondetailpage")
                    
                    else:
                        print(f"Transaction detail verified for account: {acc}", flush=True)
                        self.update_status("Accounts", [6], "Pass", 5)

                    expected_resultC = [
                        account_number_acc,
                        "Cleared Balance",
                        "Transactions"
                    ]

                    if not self.send_ussd(expected_resultC, "*", "My_Accounts", "Transaction Detail Page(Nav back)"):
                        print("No List of transaction displayed when navigating back", flush=True)
                        return

                    back2 = self.get_ussd_message()

                    expected_resultB = [
                        "My Accounts"
                        ]
                  

                    assert "My Accounts" in back2, "Did not navigate back to My Accounts page"

                    accounts = [line for line in message_text.split("\n") if "ETB" in line or "Dollar" in line]

                    if not accounts:
                      self.fail("No ETB or Dollar accounts found.")

                print("All account checks completed successfully", flush=True)

            except Exception as e:
                print("My accounts Test failed with error:", e, flush=True)

            print("My Account test compleated!", flush=True)
            print_and_clear_slow_popups(self, "My Accounts")
            self.cancel_ussd()
            time.sleep(1)

def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()
