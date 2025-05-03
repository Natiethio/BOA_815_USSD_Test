import unittest
import time
import re
import sys
import os
from Helpers.transfer_helper import transfer_helper


def atm_withdrawal(self):
        
        retries = 3
        attempt = 0
        status_atm = False
        # print("Hello this is atm_withdrawal ext")

        # self.enter_pin_to_login()

        status_helper = transfer_helper(self)

        time.sleep(5)
        print("Test for Atm With drawal ..", flush=True)


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

            #     return False
            # else:
            #     print("Failed after retries")
            #     print("No home page found retrying")
            #     self.cancel_ussd()
            #     return
            
                
        expected_ResultB = [
            "Transfer",
            "1: Transfer within BoA", 
            "2: ATM withdrawal",
            "3: Load to TeleBirr",
            "4: Transfer to M-PESA",
            "5: Awach"
            ]
        
        expected_ResultC = [ 
            "ATM withdrawal"
        ]
                
        # WebDriverWait(self.driver, 20).until(
        # EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

        status = self.send_ussd(expected_ResultB ,"2","atm_withdrawal", "BOA Accouts Lists Page")

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

            status = self.send_ussd("ATM withdrawal", selection, "atm_withdrawal", "Enter Amount Page(ATM)")

            if not status:
                print(f"Failed to select account at index {selection}", flush=True)
                continue

            message_text = self.get_ussd_message()

            account_number = account.split(":")[1].strip().split("-")[0].strip()

            status = self.send_ussd("Enter Amount(multiple of 100)", "100", "atm_withdrawal", "Please Confirm(ATM)")

            if not status:
              print("Failed to send amount for ATM withdrawal", flush=True)
              continue


            message_text = self.get_ussd_message()
            # status = self.send_ussd("Please Confirm", "1", "atm_withdrawal")
            status = self.send_ussd("Please Confirm", "*", "atm_withdrawal", "Enter Amount Page(ATM Back Nav)")


            if not status:
               print("Transaction confirmation failed", flush=True)
               self.update_status("Transfer", [12], "Fail", 5,screenshot_name="atmwithdrawal_confirmationfailed")
               self.update_status("Transfer", [12], "Atm withdrawal transaction confirmation failed", 6)
               continue
            else:
                print(f"Transaction confirmation pass for {account.strip()}", flush=True)
                self.update_status("Transfer", [12], "Pass", 5)
                time.sleep(0.5)
                status = self.send_ussd("Enter Amount(multiple of 100)", "*", "atm_withdrawal", "ATM BOA Accouts Lists Page(Back Nav)")
                if not status:
                    print("failed on else status")

            if index < len(accounts) - 1:
                    # status = self.send_ussd(expected_ResultB, "2", "atm_withdrawal")
                    final_message = self.get_ussd_message()
                    print(final_message, flush=True)
                    # if not any(x in final_message.lower() for x in ["atm withdrawal", "etb", "withdrawal"]):
                    if "atm withdrawal" not in final_message.lower():
                    # if not status:
                        print("Failed to return to ATM withdrawal menu for next account", flush=True)
                       #break

        print("ATM negative scenario test started...")

        for index, account in enumerate(accounts):

            print(f"\nChecking account: {account.strip()}", flush=True)
            selection = str(index + 1)

            # Select account
            status = self.send_ussd("ATM withdrawal", selection, "atm_withdrawal", "Enter Amount Page(ATM)")
            if not status:
                print(f"Failed to select account at index {selection}", flush=True)
                continue

            message_text = self.get_ussd_message()
            account_number = account.split(":")[1].strip().split("-")[0].strip()

            # Negative Test: Try to send 9000 birr
            print("Negative test with 9000 birr", flush=True)
            status = self.send_ussd("Enter Amount(multiple of 100)", "9000", "atm_withdrawal", "Please Confirm(ATM Negative)")

            if not status:
                print("Failed to send 9000 birr", flush=True)
                continue


            status = self.send_ussd("Please Confirm", "1", "atm_withdrawal", "ATM Single Transfer Limit Page")

            if not status:
                print("Failed to confirm", flush=True)
                continue

            message_text = self.get_ussd_message()
            print(f"Negative test message: {message_text}", flush=True)
            
            if "Amount should not be greater than birr 8000" in message_text:
                print("Negative test passed: amount over limit rejected.", flush=True)
                # Press * to go back
                status =  self.send_ussd("Amount should not be greater than birr 8000", "*", "atm_withdrawal", "Enter Amount Page(ATM Back Nav Negative)")
                if not status:
                  print("Failed go back amount page", flush=True)
                  self.update_status("Transfer", [15], "Fail", 5, screenshot_name="Atm_transferlimiybypass")
                  continue
                else:
                    self.update_status("Transfer", [15], "Pass", 5)
                    status =  self.send_ussd("Enter Amount(multiple of 100)", "*", "atm_withdrawal", "ATM BOA Accouts Lists Page(Back Nav Negative)")
                

                if not status:
                  print("Failed go back on account list page", flush=True)
                  continue

            elif "repository.productTransactionAlreadyExists" or "value too large for column" in message_text.lower:

                print("Transaction already exists or error occured, retrying same account...", flush=True)
                
                message_text = self.get_ussd_message()

                if "value too large for column" in message_text:
                   print("Un usual error")
                   status = self.send_ussd("value too large for column", "*", "atm_withdrawal", "Enter Amount Page(ATM Reversed)")

                   if not status:
                        print("unexpected on unexpected page", flush=True)
                        # self.cancel_ussd()
                        break
                   
                #    status = self.send_ussd("value too large for column", "*", "atm_withdrawal")

                   if not status:
                        print("Failed to confirm", flush=True)
                        continue

                else:
                    self.send_ussd("repository.productTransactionAlreadyExists", "*", "atm_withdrawal")
                
                while attempt < retries:
                    print(f"Negative error repository exist or unusual error retry test attempt {attempt + 1} with 9000 birr", flush=True)
                    status = self.send_ussd("Enter Amount(multiple of 100)", "9000", "atm_withdrawal", "Please Confirm(ATM Negative)")

                    if not status:
                        print("Failed to send 9000 birr", flush=True)
                        self.cancel_ussd()
                        break

                    status = self.send_ussd("Please Confirm", "1", "atm_withdrawal", "ATM Single Transfer Limit Page")

                    if "Amount should not be greater than birr 8000" in message_text:
                            print("Negative test passed: amount over limit rejected.", flush=True)
                            # Press * to go back
                            status =  self.send_ussd("Amount should not be greater than birr 8000", "*", "atm_withdrawal", "Enter Amount Page(ATM Back Nav Negative)")

                            if not status:
                              print("Failed go back on limit page", flush=True)
                              self.cancel_ussd()
                              break

                            status =  self.send_ussd("Enter Amount(multiple of 100)", "*", "atm_withdrawal", "ATM BOA Accouts Lists Page(Back Nav Negative)")

                            if not status:
                              print("Failed go back on account list page", flush=True)
                              self.cancel_ussd()
                              break

                            break
                    
                    attempt += 1

                else:
                  print("Exceeded retries for repository.productTransactionAlreadyExists", flush=True)
                  self.update_status("Transfer", [15], "Fail", 5, screenshot_name="fail_overlimit_atmtra")
                  self.update_status("Transfer", [15], "repository already exists error", 6)
                  self.cancel_ussd()  
                  return False      
            # else:
            #     print("Unexpected error occurred in negative test", flush=True)
            #     self.send_ussd_input("*") 
            #     self.cancel_ussd() 


            if index < len(accounts) - 1:
                    # status = self.send_ussd(expected_ResultB, "2", "atm_withdrawal")
                    final_message = self.get_ussd_message()
                    print(final_message, flush=True)
                    # if not any(x in final_message.lower() for x in ["atm withdrawal", "etb", "withdrawal"]):
                    if "atm withdrawal" not in final_message.lower():
                    # if not status:
                        print("Failed to return to ATM withdrawal menu for next account", flush=True)
                        break
            else:
                print("All ATM tests Compleated",flush=True)
        
        # print("ATM Transfer Ends")
        self.cancel_ussd()
        # return False
                




