
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


def exchange_rates(self):
            try:
                self.enter_pin_to_login()
                
                input_field = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.android.phone:id/input_field']"))
                )
                input_field.clear()

                expected_result = [
                    "Welcome to BOA Mobile Banking",
                    "7: Exchange Rates"
                ]

                if not self.send_ussd(expected_result, "7", "Exchange_Rates", "Exchange Rates Lists Page"):
                    print("No Home page found Exiting", flush=True)
                    return


                message_text = self.get_ussd_message()

                print("USSD Response:", message_text, flush=True)

                assert "Exchange Rates" in message_text , "Did not land on the expected 'Exchange Rates' page"
                print("Here 1")
                currencies = [line for line in message_text.split("\n")if ":" in line]
                print(currencies, flush=True)
                
                if not currencies:
                  self.update_status("setting", [2], "Fail", 5, screenshot_name="exchange_rates_nocurrenciesfound")
                  self.fail("No currencies found.")
                else:
                  print("list of currencies are displayed", flush=True)
                  self.update_status("setting", [2], "Pass", 5) #pass
        
                  print("Excel status Updated", flush=True)
                print(f"{len(currencies)} currency(ies) found: {currencies}", flush=True)

                for i, curr in enumerate(currencies, start=1):

                    curr = curr.split(":")[1].strip()
                    print(f"\nChecking currencies {i}: {curr}", flush=True)

                    expected_resultB = [
                        "Exchange Rates"
                        ]

                    if not self.send_ussd(expected_resultB, str(i), "Exchange_Rates", "exchange rates Page"):
                        print("No exchange rates found terminating exchange rates operation", flush=True)
                        return
                    
                    expected_resultC = [
                        "Info Buy Rate:",
                        "Sell Rate:",
                    ]

                    if not self.send_ussd(expected_resultC, "*", "Exchange_Rates", "exchange rates Detail Page"):
                        print("No List of exchange rates displayed", flush=True)
                        self.update_status("setting", [2], "Fail", 5, screenshot_name="no_exchange_rates_list_found")
                    
                    else:
                        print("The list of exchange rates is displayed", flush=True)
                        self.update_status("setting", [2], "Pass", 5)

                    expected_result = [
                        "Welcome to BOA Mobile Banking",
                        "7: Exchange Rates"
                    ]
                  
                    if not self.send_ussd(expected_result, "7", "Exchange_Rates", "Exchange Rates Lists Page"):
                        print("No Home page found Exiting", flush=True)
                        return


                    back2 = self.get_ussd_message()


                    assert "Exchange Rates" in message_text , "Did not land on the expected 'Exchange Rates' page"

                    currencies = [line for line in message_text.split("\n") if ":" in line]

                    if not currencies:
                      self.fail("No currencies found.")

                print("All currencies checks completed successfully", flush=True)

            except Exception as e:
                print("Exchange Rates Test failed with error:", e, flush=True)

            print("Exchange Rates test compleated!", flush=True)
            print_and_clear_slow_popups(self, "Exchange Rates")
            self.cancel_ussd()
            time.sleep(1)

def print_and_clear_slow_popups(self, func_name):
    if self.slow_popups:
        print(f"\n[Slow Popups in {func_name}]")
        for page, duration in self.slow_popups:
            print(f"{page}: {duration}s")
        self.slow_popups.clear()
