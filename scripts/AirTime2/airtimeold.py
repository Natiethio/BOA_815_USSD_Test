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

def airtime_helper(self):

        # self.enter_pin_to_login()

        print("Test for Airtime..", flush=True)

        expected_Result = [
              "1: My Accounts",
              "2: Transfer",
              "3: Transfer to Other Bank",
              "4: Transfer to Own",
              "5: Airtime",
              "6: Utilities",
              "7: Exchange Rates",
              "8: More options"
            ]
        
        WebDriverWait(self.driver, 50).until(
         EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_Result ,"5","Airtime")

        return status

def airtime(self):
        print("Hello this is airtime ext")
        print(self.pin)
        print(self.phone_number)

        # self.enter_pin_to_login()

        status_helper = airtime_helper(self)

        time.sleep(1)
        # print("Test for Airtime ..", flush=True)


        retries = 3

        for _ in range(retries):
            status_helper = airtime_helper(self)
            if status_helper:
                break
            else:
                print("Home page not matched retrying...", flush=True)
            
            if not status_helper:
                print("Failed after retries",flush=True)
                print("No home page found retrying",flush=True)
                self.cancel_ussd()
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
            self.update_status("Airtime topup", [2], "Fail", 5 , screenshot_name="no_airtime_hostfound")
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)
        else:
            self.update_status("Airtime topup", [2], "Pass", 5)

        message_text = self.get_ussd_message()

        # assert "ATM withdrawal" in message_text , "Did not land on the expected 'ATM withdrawal' page"

        accounts = [line for line in message_text.split("\n") if "ETB" in line or "Dollar" in line]

        if not accounts:
            self.fail("No ETB or Dollar accounts found.")
        else:
            print(f"{len(accounts)} account(s) found: {accounts}", flush=True)

        for index, account in enumerate(accounts):
            print(f"\nChecking account: {account.strip()}", flush=True)
            selection = str(index + 1)

            status = self.send_ussd("EthioTelecom Airtime", selection, "EthioTelecom Airtime")

            if not status:
                print(f"Failed to select account at index {selection}", flush=True)
                continue

            message_text = self.get_ussd_message()

            account_number = account.split(":")[1].strip().split("-")[0].strip()

            phone = self.phone_number
            

            
            print("Entering account number {phone}", flush=True)

            status = self.send_ussd("Enter Recharge Phone No", phone, "EthioTelecom Airtime")

            if not status:
              print("Failed to send phone for EthioTelecom Airtime", flush=True)
              continue
            amount = self.amount

            status = self.send_ussd("Enter Amount", amount, "EthioTelecom Airtime")

            if not status:
              print("Failed to send amount for EthioTelecom Airtime", flush=True)
              continue


            message_text = self.get_ussd_message()
            # status = self.send_ussd("Please Confirm", "1", "atm_withdrawal")
            status = self.send_ussd("Please Confirm", "*", "airtime")


            if not status:
               print("airtime confirmation failed", flush=True)
               self.update_status("Airtime topup", [5], "Fail", 5 , screenshot_name="airtime_conffaild")
               continue
            else:
                print(f"airtime confirmation pass for {account.strip()}", flush=True)
                self.update_status("Airtime topup", [5], "Pass", 5)
                time.sleep(0.5)
                status = self.send_ussd("Enter Amount", "*", "airtime")
                if not status:
                    print("failed on else status")
            
            # status = self.send_ussd("Complete", "*", "atm_withdrawal")
            # print("Atm Transfer Successfully for", flash=True)



            # if status:
            #     self.update_status("Transfer", [12], "Pass", 7)
            # else:
            #     self.update_status("Transfer", [12], "Fail", 7)

            if index < len(accounts) - 1:
                    # status = self.send_ussd(expected_ResultB, "2", "atm_withdrawal")
                    final_message = self.get_ussd_message()
                    print(final_message, flush=True)
                    # if not any(x in final_message.lower() for x in ["atm withdrawal", "etb", "withdrawal"]):
                    if "Airtime".lower()  not in final_message.lower():
                    # if not status:
                        print("Failed to return to ATM withdrawal menu for next account", flush=True)
                        break
       
        print("Airtime for all account Compleated", flush=True)
        self.cancel_ussd()