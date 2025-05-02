def extract_staff_or_saving_option(self, ussd_text):
        lines = ussd_text.split('\n')
        for line in lines:
            if "STAFF" in line.upper() or "SAVING" in line.upper():
                if ":" in line:
                    option_number =  line.split(":")[0].strip()
                    account_number_ext = line.split(":")[1].split("-")[0].strip()
                    return option_number, account_number_ext
        return None, None