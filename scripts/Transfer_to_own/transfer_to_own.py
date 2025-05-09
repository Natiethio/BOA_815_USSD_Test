import unittest
import time
import re
import sys
import os
from Helpers.extract_staff_or_saving_option import extract_staff_or_saving_option, extract_apol_option



def transfer_to_own_account(self):
    print("Test for Transfer to Own Account")


    self.enter_pin_to_login()


    print("Test for Transfer to Own Account..", flush=True)

    expected_menu = [
              "1: My Accounts",
              "2: Transfer",
              "3: Transfer to Other Bank",
              "4: Transfer to Own",
              "5: Airtime",
              "6: Utilities",
              "7: Exchange Rates",
              "8: More options"
    ]

    if not self.send_ussd(expected_menu, "4", "Transfer to Own", "BOA Accounts list Page(Ethiotelecom Air Time)"):
        print("No Home page found Exiting", flush=True)
        return

    message_text = self.get_ussd_message()
    account_option, account_number = extract_staff_or_saving_option(self, message_text)
    if not account_option:
        print("No valid STAFF or SAVING account found", flush=True)
        self.cancel_ussd()
        return

    print(f"Processing account: {account_number}", flush=True)
    if not self.send_ussd(["Transfer to Own"], account_option, "Transfer to Own", "Funds Transfer Own Account Page(Transfer to Own)"):
        print("Failed to select account", flush=True)
        return
    
    message_text = self.get_ussd_message()
    account_option, account_number = extract_apol_option(self, message_text)
    if not account_option:
        print("No valid Appolo account found", flush=True)
        self.cancel_ussd()
        return

    print(f"Processing account: {account_number}", flush=True)
    if not self.send_ussd(["Funds Transfer Own Account"], account_option, "Transfer to Own", "Press any key for more Page(Transfer to Own)"):
        print("Failed to select account", flush=True)
        return
    
    
    print("Test for Even if the commulative is reached own account transfer should work with any amount negative scenario..",  flush=True)

    # Press any key for more

    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Amount Page(Transfer to Own)")

    if not status:
        print("Failed to send any key for more", flush=True)
        return
    # Enter amount
    status = self.send_ussd(["Enter Amount"], "1000000", "Transfer to Own", "Press any key for more Page(Transfer to Own)")

    if not status:
        print("Failed to send amount for Transfer to Own", flush=True)
        return
        
    # Press any key for more

    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Reason Page(Transfer to Own)")

    if not status:
            print("Failed to send any key for more", flush=True)
            return

    # Enter reason
    status = self.send_ussd(["Enter Reason"], "Test", "Transfer to Own", "Press any key for more Page(Transfer to Own)")

    if not status:
        print("Failed to send reason for Transfer to Own", flush=True)
        return
    
    # Press any key for more
    status = self.send_ussd(["Press any key for more"], "q" , "Transfer to Own", "Review Page(Transfer to Own)")
    
    if not status:
            print("Failed to send any key for more", flush=True)
            return
    # Please Confirm
    status = self.send_ussd(["1: Yes"], "1", "Transfer to Own", "Confirmation Page(Transfer to Own)")

    if not status:
        print("Failed to send confirmation for Transfer to Own", flush=True)
        return
    
    response = self.get_ussd_message()

    status = self.send_ussd(["System Error, Please call 8397 for more."], "*", "Transfer to Own", "Press any key for more Page(Transfer to Own)")


    if not status:
        print("Even if the commulative is reached own account transfer should work with any amount. checking possible cases and retrying..", flush=True)


        if "repository.productTransaction" in response or "productTransactionAlreadyExists" in response or "value too large for column" in response:
      
            max_retries = 3
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                    print(f"Attempt {retry_count + 1} for Transfer to Own", flush=True)

                    response = self.get_ussd_message()

                    # print(f"Recoverable error encountered: {response}", flush=True)

                    self.send_ussd_input("*")

                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Amount Page(Transfer to Own)")

                    if not status:
                        print("Failed to send any key for more", flush=True)
                        return

                    # Enter amount
                    status = self.send_ussd(["Enter Amount"], "1000000", "Transfer to Own", "Press any key for more Page(Transfer to Own)")
                    if not status:
                        print("Failed to enter amount over limit", flush=True)
                        return
                   
                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Reason Page(Transfer to Own)")

                    if not status:
                        print("Failed to confirm over transaction", flush=True)
                        return
                    
                    # Enter reason
                    status = self.send_ussd(["Enter Reason"], "Test", "Transfer to Own", "Press any key for more Page(Transfer to Own)")

                    if not status:
                        print("Failed to send reason for Transfer to Own", flush=True)
                        return
                    
                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "q" , "Transfer to Own", "Review Page(Transfer to Own)")
                    
                    if not status:
                            print("Failed to send any key for more", flush=True)
                            return
                    # Please Confirm
                    status = self.send_ussd(["1: Yes"], "1", "Transfer to Own", "Confirmation Page(Transfer to Own)")

                    if not status:
                        print("Failed to send confirmation for Transfer to Own", flush=True)
                        return

                    response = self.get_ussd_message()

                    if "System Error, Please call 8397 for more." in response:
                        print("Even if the commulative is reached own account transfer is working with any amount", flush=True)
                        self.update_status("Transfer", [75], "Pass", 5)
                        self.send_ussd_input("*")
                        success = True
                        break
                    else:
                        print("Failed to validate even if the commulative is reached own account transfer is working with any amount retrying...", flush=True)
                        # self.update_status("Transfer", [75], "Fail", 5)
                        # self.send_ussd_input("*")
                        continue

            if not success:
                print("Even if the commulative is reached own account transfer is working with any amount failed after retries", flush=True)
                self.send_ussd_input("*")
                self.update_status("Transfer", [75], "Fail", 5)
        
        
        else:
            print("Failed to validate even if the commulative is reached own account transfer is working with any amount b/c of unknown page result continuing to Positive Test", flush=True)
            self.send_ussd_input("*")
            self.update_status("Transfer", [75], "Fail", 5)

    else:
        print(f"Even if the commulative is reached own account transfer is working with any amount passed successfully: {account_number}", flush=True)
        # self.send_ussd_input("*")
        self.update_status("Transfer", [75], "Pass", 5)

    # Test for Transfer to Own Account with Positive Test..
    print("Test for Transfer to Own Account with Positive Test..",  flush=True)

    # Press any key for more

    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Amount Page(Transfer to Own)")

    if not status:
        print("Failed to send any key for more", flush=True)
        return
    # Enter amount
    amount = self.amount
    status = self.send_ussd(["Enter Amount"], amount, "Transfer to Own", "Press any key for more Page(Transfer to Own)")

    if not status:
        print("Failed to send amount for Transfer to Own", flush=True)
        return
        
    # Press any key for more

    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Reason Page(Transfer to Own)")

    if not status:
            print("Failed to send any key for more", flush=True)
            return

    # Enter reason
    status = self.send_ussd(["Enter Reason"], "Test", "Transfer to Own", "Press any key for more Page(Transfer to Own)")

    if not status:
        print("Failed to send reason for Transfer to Own", flush=True)
        return
    
    # Press any key for more
    status = self.send_ussd(["Press any key for more"], "q" , "Transfer to Own", "Review Page(Transfer to Own)")
    
    if not status:
            print("Failed to send any key for more", flush=True)
            return
    # Please Confirm
    status = self.send_ussd(["1: Yes"], "1", "Transfer to Own", "Confirmation Page(Transfer to Own)")

    if not status:
        print("Failed to send confirmation for Transfer to Own", flush=True)
        return
    
    response = self.get_ussd_message()

    status = self.send_ussd(["Complete"], "*", "Transfer to Own", "Press any key for more Page(Transfer to Own)")


    if not status:
        print("Transfer to Own Account with Positive Test failed", flush=True)


        if "repository.productTransaction" in response or "productTransactionAlreadyExists" in response or "value too large for column" in response:
      
            max_retries = 3
            retry_count = 0
            success = False

            while retry_count < max_retries and not success:
                    print(f"Attempt {retry_count + 1} for Transfer to Own", flush=True)

                    response = self.get_ussd_message()

                    # print(f"Recoverable error encountered: {response}", flush=True)

                    self.send_ussd_input("*")

                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Amount Page(Transfer to Own)")

                    if not status:
                        print("Failed to send any key for more", flush=True)
                        return

                    # Enter amount
                    amount = self.amount
                    status = self.send_ussd(["Enter Amount"],amount, "Transfer to Own", "Press any key for more Page(Transfer to Own)")
                    if not status:
                        print("Failed to enter amount over limit", flush=True)
                        return
                   
                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "1" , "Transfer to Own", "Enter Reason Page(Transfer to Own)")

                    if not status:
                        print("Failed to confirm over transaction", flush=True)
                        return
                    
                    # Enter reason
                    status = self.send_ussd(["Enter Reason"], "Test", "Transfer to Own", "Press any key for more Page(Transfer to Own)")

                    if not status:
                        print("Failed to send reason for Transfer to Own", flush=True)
                        return
                    
                    # Press any key for more
                    status = self.send_ussd(["Press any key for more"], "q" , "Transfer to Own", "Review Page(Transfer to Own)")
                    
                    if not status:
                            print("Failed to send any key for more", flush=True)
                            return
                    # Please Confirm
                    status = self.send_ussd(["1: Yes"], "1", "Transfer to Own", "Confirmation Page(Transfer to Own)")

                    if not status:
                        print("Failed to send confirmation for Transfer to Own", flush=True)
                        return

                    response = self.get_ussd_message()

                    if "Complete" in response:
                        print("Transfer to Own Account Complited Successfully", flush=True)
                        self.update_status("Transfer", [72], "Pass", 5)
                        self.send_ussd_input("*")
                        success = True
                        break
                    else:
                        print("Failed to Transfer to Own Account retrying...", flush=True)
                        # self.update_status("Transfer", [72], "Fail", 5)
                        # self.send_ussd_input("*")
                        continue

            if not success:
                print("Transfer to Own Account failed after retries", flush=True)
                self.send_ussd_input("*")
                self.update_status("Transfer", [72], "Fail", 5)
        
        
        else:
            print("Transfer to Own Account failed", flush=True)
            self.send_ussd_input("*")
            self.update_status("Transfer", [72], "Fail", 5)

    else:
        print(f"Transfer to Own Account passed successfully: {account_number}", flush=True)
        # self.send_ussd_input("*")
        self.update_status("Transfer", [72], "Pass", 5)
        time.sleep(0.5)

    print("Transfer to Own Account Test completed!", flush=True)
    self.cancel_ussd()
    # return True