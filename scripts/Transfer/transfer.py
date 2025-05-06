from Transfer.Transfer_Withen_BOA.transfer_within_BOA import transfer_within_BOA
from Transfer.ATM_Withdrawal.atm_withdrawal import atm_withdrawal
from Transfer.Transfer_to_MPESA.transfer_to_mpesa import transfer_to_mpesa
from Transfer.Load_to_TeleBirr.load_to_telebirr import load_to_telebirr

def transfer(self, transfer_sub_module):
        

        try:
            # self.enter_pin_to_login()
             
            match transfer_sub_module:
                case "1":
                    result = transfer_within_BOA(self)
                    print("Transfer within BOA completed" if result else "Transfer within BOA failed", flush=True)


                case "2":
                    result = atm_withdrawal(self)
                    print("ATM Withdrawal completed" if result else "ATM Withdrawal failed", flush=True)

                case "3":
                    result = load_to_telebirr(self)
                    print("Load to TeleBirr completed" if result else "Load to TeleBirr failed", flush=True)

                case "4":
                    result = transfer_to_mpesa(self)
                    print("Transfer to M-PESA completed" if result else "Transfer to M-PESA failed", flush=True)

                case _:  
                    print("Executing all transfer submodules...", flush=True)
                    
                    transfer_within_BOA(self)
                    atm_withdrawal(self)
                    load_to_telebirr(self)
                    transfer_to_mpesa(self)  

        except Exception as e:
          print(f"[Transfer Module Error] {e}", flush=True)





        # transfer_withen_BOA = transfer_within_BOA(self)
        # if transfer_withen_BOA:
        #     print("Transfer with boa complated",flush=True)
        # else:
        #      print("Transfer with boa failed",flush=True)

        # atm_withdrawal_one = atm_withdrawal(self)

        # load_to_telebirrtest = load_to_telebirr(self)

        # transfer_to_mpesatest = transfer_to_mpesa(self)
        # if not success:
        #     print("ATM Withdrawal failed. Stopping further tests.", flush=True)