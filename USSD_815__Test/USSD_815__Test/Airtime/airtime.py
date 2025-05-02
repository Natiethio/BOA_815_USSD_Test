import unittest
import time
import re
import sys
import os

def airtime(self):
        print("Hello this is airtime ext")
        print(self.pin)
        print(self.phone_number)
        # phone_number   = sys.argv[6] if len(sys.argv) > 6 else "0970951608"
        # amount         = sys.argv[5] if len(sys.argv) > 5 else "10"
        # self.enter_pin_to_login()

        status_helper = self.airtime_helper()

        time.sleep(5)
        print("Test for Airtime ..", flush=True)

        # status_helper = self.airtime_helper()

        if not status_helper:
            print("No home page found retrying")
            self.cancel_ussd()
            airtime(self)
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
            self.update_status("Airtime topup", [2], "Fail", 7)
            # self.driver.quit()
            # return
            print("All expected value not found",flush=True)

        self.update_status("Airtime topup", [2], "Pass", 7)

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
               self.update_status("Airtime topup", [5], "Fail", 7)
               continue
            else:
                print(f"airtime confirmation pass for {account.strip()}", flush=True)
                self.update_status("Airtime topup", [5], "Pass", 7)
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