def transfer_within_BOA(self):

        #self.enter_pin_to_login
        
        status_helper = self.transfer_helper()
        print("Test for Transfer withen BoA", flush=True)

        if status_helper:
                
                expected_ResultB = [
                    "Transfer",
                    "1: Transfer within BoA", 
                    "2: ATM withdrawal",
                    "3: Load to TeleBirr",
                    "4: Transfer to M-PESA",
                    "5: Awach"
                    ]
                
                WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

                status = self.send_ussd(expected_ResultB ,"1","transfer_with_boa")

                if status:
                 self.update_status("Transfer", [2], "Pass", 7)
                else:
                 self.update_status("Transfer", [2], "Fail", 7)
                 self.driver.quit()
                 exit()

                expected_ResultC = [
                    "Enter Account No"
                    ]
                
                for attempt in range(1, 4):
                    time.sleep(0.5)
                    # accountno = input("Enter Account Number:")
                    accountno = account_number
                    print("Account Number", flush=True)

                    WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))


                    status = self.send_ussd(expected_ResultC ,accountno,"transfer_with_boa")


                    expected_ResultD = ["Transfer within BoA"]

                    txn_text = self.get_ussd_message()

                    print("USSD message for accounts:\n", txn_text, flush=True)

                    account_option, detected_account = self.extract_staff_or_saving_option(txn_text)

                    if not account_option or not detected_account:
                        print("Invalid or no STAFF or SAVING account found. Retrying...", flush=True)
                        self.send_ussd_input("*")

                        WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                        
                        self.send_ussd(expected_ResultB, "1", "transfer_with_boa")
                        continue

                    if accountno == detected_account:
                        print("Destination account cannot be the same as the source account.", flush=True)
                        if attempt == 3:
                            self.cancel_ussd()
                            return
                        self.send_ussd_input("*")

                        WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                        
                        self.send_ussd(expected_ResultB, "1", "transfer_with_boa")
                        continue

                    print(f"STAFF/SAVING account found. Selecting option {account_option}.", flush=True)

                    WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

                    self.send_ussd(expected_ResultD, account_option, "transfer_with_boa")
                    break

                fixed_amounts = [600000, 501000, None]  
                round_num = 1

                # while True:
                for test_amount in fixed_amounts:
                
                  while True:
                    
                    while True:

                        expected_ResultE = ["Enter Amount"]
                        # amount_etb = input("Please Enter Amount less than 500k: ")

                        if test_amount is not None:
                            amount_etb = str(test_amount)
                            print(f"Test Round {round_num}: Using fixed test amount {amount_etb}", flush=True)
                        else:
                            WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message"))
                            )
                            user_input = amount
                            # user_input = input("Enter transfer amount (or press Enter for default 20): ").strip()
                            amount_etb = user_input if user_input.isdigit() else "20"

                        if not amount_etb.isdigit() or int(amount_etb) <= 0:
                            print("Amount should be a number. Try again.", flush=True)
                            continue

                        if int(amount_etb) >= 500000:
                          print("Testing over-limit Negative scenario.", flush=True)

                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

                        status = self.send_ussd(expected_ResultE, amount_etb, "transfer_with_boa")
                        if status:
                            break


                    while True:
                            expected_ResultF = ["Enter Remark"]
                            # remark = input("Please Enter Remark: ")
                            remark ="pay"


                            if not remark.replace(" ", "").isalpha():
                                print("Remark should only contain letters and spaces.", flush=True)
                                continue

                            WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                            
                            if self.send_ussd( expected_ResultF, remark, "transfer_with_boa"):
                             break

                    while True:
                        expected_ResultG = ["Please Confirm"]

                        WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

                        # confirm = input("Please Confirm (1 for Yes / 2 for No): ").strip()
                        confirm = "1"

                        if confirm not in ["1", "2"]:
                            print("Invalid input. Enter 1 or 2.", flush=True)
                            continue

                        WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))

                        self.send_ussd(expected_ResultG, confirm, "transfer_with_boa")

                        if confirm == "2":
                            print("Restarting from amount entry...", flush=True)
                            break  # Back to amount entry

                        break  # Valid confirmation, move on

                    if confirm == "1":

                        final_message = self.get_ussd_message()
                        print("Final message:\n", final_message.lower(), flush=True)

                        try:

                            if "you have exceeded the daily transaction limit." in final_message.lower():
                                print("Cumulative transfer limit exceeded. Try smaller amount.", flush=True)
                                self.update_status("Transfer", [8], "Pass", 7)
                                expected_ResultF = ["you have exceeded the daily transaction limit."]
                                WebDriverWait(self.driver, 25).until(
                                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                                status = self.send_ussd(expected_ResultF, "*", "transfer_with_boa")
                                round_num += 1
                                break


                            elif "you have exceeded the single transaction limit." in final_message.lower():
                                print("Single transaction limit exceeded. Try smaller amount.", flush=True)
                                self.update_status("Transfer", [9], "Pass", 7)
                                expected_ResultF = ["you have exceeded the single transaction limit."]
                                WebDriverWait(self.driver, 25).until(
                                EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                                status = self.send_ussd(expected_ResultF, "*", "transfer_with_boa")
                                round_num += 1
                                break


                            elif "complete" in final_message.lower() and self.extract_and_validate_success_screen(final_message):
                                if round_num == 1:
                                    self.update_status("Transfer", [8], "Fail", 7)
                                    break

                                else:
                                    print("Transaction was successful.", flush=True)
                                    self.update_status("Transfer", [5], "Pass", 7)
                                    expected_ResultF = ["Complete"]

                                    WebDriverWait(self.driver, 25).until(
                                    EC.presence_of_element_located((AppiumBy.ID, "com.android.phone:id/message")))
                                    
                                    status = self.send_ussd(expected_ResultF, "*", "transfer_with_boa") # not nessesary
                                    time.sleep(0.2)
                                    break

                            else:
                                print("repository exists", flush=True)
                                self.cancel_ussd()
                                time.sleep(0.5)
                                self.enter_pin_to_login()
                                break

                        except:
                            print("Unexpected message received. Marking as failed.", flush=True)
                            self.update_status("Transfer", [5], "Fail", 7)
                            break 

                    # round_num += 1
                    

                print("Cancel Pressed", flush=True)
                self.cancel_ussd()
                time.sleep(0.5)
        else:
            print("Error on transfer helper retrying..", flush=True)
            for attempt in range(1,3):
               
               if status_helper:
                   break
               
               self.transfer_within_BOA()  