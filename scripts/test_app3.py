import unittest
import time
import os
import pandas as pd
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

# 182975435
class BankingAppTest(unittest.TestCase):

    def setUp(self) -> None:
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = "R9ZR601C18H"
        options.udid = "R9ZR601C18H"
        options.app_package = "cn.tydic.ethiopay"
        options.app_activity = "com.huawei.digitalpayment.customer.login_module.login.LoginFirstActivity"
        options.no_reset = True
        options.language = "en"
        options.locale = "US"

        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.driver.implicitly_wait(5)

    def tearDown(self) -> None:
      if self.driver:
        self.driver.quit()


    def enter_pin_to_login(self):
        if self.driver.wait_activity("com.huawei.digitalpayment.customer.login_module.login.LoginFirstActivity", 10):
            print("Phone Login detected....")

            try:
                phone_number = input("Please Enter Your Phone Number:")
                phone_input = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
                phone_input.clear()
                phone_input.send_keys(phone_number)
                time.sleep(1)

                next_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Next']")
                next_button.click()
                print("Next Button Detected")


            except Exception as e:
                print(f"Error Cant find input: {e}")
                self.fail("Phone number input failed.")
                return
            
        count = 0 
        while count <= 3:

            if self.driver.wait_activity("com.huawei.digitalpayment.customer.login_module.login.PinOfLoginActivity", 10):

                if (count == 2):
                    print("Wrong One Chance Left")
                elif (count == 3):
                    print("User Locked") 
                    break 

                if (count == 3):
                    print("User Locked")
                    self.driver.quit()
                    exit()
                    break

                print("PIN Screen Detected")

                if self.driver.find_element(AppiumBy.XPATH, f"//android.view.ViewGroup[@resource-id='cn.tydic.ethiopay:id/pin_input_keyboard']"):
                  print("Keyboard Detected")

                  pin = input("Pleace Enter your PIN: ")

                  try:
                            # pin = "109308"
                        for digit in pin:
                            key = self.driver.find_element(AppiumBy.XPATH, f"//android.widget.TextView[@resource-id='cn.tydic.ethiopay:id/tv_input_{digit}']")
                            key.click()
                            time.sleep(0.3)  


                  except Exception as e:
                        print(f"Error entering PIN: {e}")
                        # self.driver.quit()
                        # exit()
                        continue

                print("Waiting for Home Screen...")
                time.sleep(4)

                if self.driver.wait_activity("com.huawei.digitalpayment.customer.homev6.activity.HomeActivity", 10):
                   print("Logged in Successfully")
                   break
                else:
                    # self.driver.quit()
                    # exit()
                    print("Wrong Password Please try again.")
                    count += 1

    def check_home_component(self):

            print("Checking Home Page Components...\n")

            components = {

                "Logo Box": [
                    "//android.widget.LinearLayout[@resource-id='cn.tydic.ethiopay:id/ll_logo']",
                    "//android.widget.LinearLayout[@resource-id='cn.tydic.ethiopay:id/ll_logo']/android.widget.LinearLayout/android.widget.ImageView[1]",
                    "//android.widget.LinearLayout[@resource-id='cn.tydic.ethiopay:id/ll_logo']/android.widget.LinearLayout/android.widget.ImageView[2]",
                ],

                "Account Dashboard": [
                    "//android.view.ViewGroup[@resource-id='cn.tydic.ethiopay:id/home_header']",
                    "//android.widget.ImageView[@resource-id='cn.tydic.ethiopay:id/ivBackgroundVein']",
                    "//android.widget.ImageView[@resource-id='cn.tydic.ethiopay:id/ivUserHead']",
                    "//android.widget.TextView[@resource-id='cn.tydic.ethiopay:id/tvTips']",
                    "//android.widget.LinearLayout[@resource-id='cn.tydic.ethiopay:id/llLanguage']",
                    "//android.widget.TextView[@resource-id='cn.tydic.ethiopay:id/tvBalance']",
                    "//android.widget.ImageView[@resource-id='cn.tydic.ethiopay:id/ivBalanceEye']",
                    "//android.widget.TextView[@resource-id='cn.tydic.ethiopay:id/tvBalanceValue']",
                ],

            }

            results = []

            for component_name, xpath_list in components.items():
                found_all = True  
                missing_elements = []  

                for xpath in xpath_list:
                    try:
                        self.driver.find_element(AppiumBy.XPATH, xpath)
                    except:
                        found_all = False
                        missing_elements.append(xpath)

                status = "Found" if found_all else f"Not Found ({len(missing_elements)} missing)"
                results.append([component_name, status])

                print(f"{component_name}: {status}")

            self.save_results_to_excel(results)


    def save_results_to_excel(self, results):
        file_path = "test_results.xlsx"
        df = pd.DataFrame(results, columns=["Component", "Existence"])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)
        print("Test results saved to 'test_results.xlsx'")


    def test_app(self):
        try:
            self.enter_pin_to_login()
            self.check_home_component()
        except Exception as e:
            print(f"Error: {e}")
            self.fail("Login process failed.")


if __name__ == '__main__':
    unittest.main()

# adb shell pm list packages
# adb shell dumpsys window | findstr mCurrentFocus
# com.boa.boaMobileBanking