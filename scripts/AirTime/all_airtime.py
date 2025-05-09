from AirTime.airtime import airtime_topup_for_ethio_telecom, airtime_topup_for_safaricom

def airtime(self, airtime_sub_module):
        

        try:
            # self.enter_pin_to_login()
            
            match airtime_sub_module:
                case "1":
                    result = airtime_topup_for_ethio_telecom(self)
                    print("Airtime topup for ethio telecom completed" if result else "Airtime topup for ethio telecom failed", flush=True)


                case "2":
                    result = airtime_topup_for_safaricom(self)
                    print("Airtime topup for safaricom completed" if result else "Airtime topup for safaricom failed", flush=True)


                case _:  
                    print("Executing all Airtime submodules...", flush=True)
                    airtime_topup_for_ethio_telecom(self)
                    airtime_topup_for_safaricom(self)

        except Exception as e:
          print(f"[Airtime Module Error] {e}", flush=True)