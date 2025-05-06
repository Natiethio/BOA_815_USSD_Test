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
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option
from Transfer_otherBank.Instant_Transfer.instant_transfer import instant_transfer
from Transfer_otherBank.Non_Instant_Transfer.non_instant_transfer import non_instant_transfer

def otherbank(self, transfer_to_otherbank_sub_module):
    try:
    #    self.enter_pin_to_login()
       match transfer_to_otherbank_sub_module:
           case "1":
               result = instant_transfer(self)
               print("Instant Transfer Compleated", flush=True)
           case "2":
               result = non_instant_transfer(self)
               print("Non Instant Transfer Compleated", flush=True)
           case _:  
                    print("Executing all transfer to other bank submodules...", flush=True)
                    instant_transfer(self)
                    non_instant_transfer(self)

    except Exception as e:
        print(f"[Transfer Module Error] {e}", flush=True)