# from appium import webdriver
# from appium.options.android import UiAutomator2Options 
# from appium.webdriver.common.appiumby import AppiumBy
# import time

# options = UiAutomator2Options()  
# options.platform_name = "Android"
# options.device_name = "R9ZR601C18H"  
# options.app_package = "com.linkedin.android"
# options.app_activity = "com.linkedin.android.infra.navigation.MainActivity"
# options.automation_name = "UiAutomator2"
# options.no_reset = True

# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# time.sleep(5)

# try:
#     google_sign_in_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Sign in with Google')]")
#     google_sign_in_btn.click()
#     print("Clicked Google Login Button!")
# except:
#     print("Google Login Button not found!")

# time.sleep(5)

# print("Switching to Google Sign-In screen...")
# driver.wait_activity("com.google.android.gms.auth.api.credentials.assistedsignin.ui.GoogleSignInActivity", 10)

# try:
#     google_account = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'natman093@gmail.com')]")
#     google_account.click()
#     print("Selected Google Account!")
# except:
#     print("Google account not found. Entering email manually.")

# try:
#     email_input = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
#     email_input.send_keys("natman093@gmail.com")
#     next_btn = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next')]")
#     next_btn.click()
#     print("Entered email and clicked Next!")
# except:
#     print("Could not enter email.")

# time.sleep(5)

# driver.activate_app("com.linkedin.android")
# print("Switched back to LinkedIn!")

# time.sleep(5)

# driver.quit()


count = 0 

while count <= 3:
     
     if (count == 2):
          print("Wrong One Chance Left")
     elif (count == 3):
           print("User Locked") 
           break  
     
     pin = input("Enter Pin ..")


     if(pin == "2025"):
        print("Success full Login Successfully")
        break
     
     count += 1
     print(f"Iteration no{count}")
    
     
