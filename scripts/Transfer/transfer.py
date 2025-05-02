from Transfer.Transfer_Withen_BOA.transfer_within_BOA import transfer_within_BOA
from Transfer.ATM_Withdrawal.atm_withdrawal import atm_withdrawal

def transfer(self):
        transfer_withen_BOA = transfer_within_BOA(self)
        if transfer_withen_BOA:
            print("Transfer with boa complated",flush=True)
        else:
             print("Transfer with boa failed",flush=True)

        atm_withdrawal_one = atm_withdrawal(self)
        # if not success:
        #     print("ATM Withdrawal failed. Stopping further tests.", flush=True)