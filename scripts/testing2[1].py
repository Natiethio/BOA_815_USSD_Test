from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Helper function to wait for expected output
def wait_for_expected_output(expected_text, timeout=10):
    try:
        output_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{expected_text}")')
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(output_locator))
        print(f"[✓] Matched expected output: '{expected_text}'")
        return True
    except:
        print(f"[✗] Expected output NOT matched: '{expected_text}'")
        return False

# Helper function to send input after verifying expected output
def send_input(expected_text, input_value):
    if wait_for_expected_output(expected_text):
        input_field_locator = (AppiumBy.XPATH, '//android.widget.EditText')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(input_field_locator))
        input_field = driver.find_element(*input_field_locator)
        input_field.send_keys(input_value)

        send_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Send")')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(send_button_locator))
        send_button = driver.find_element(*send_button_locator)
        send_button.click()
        time.sleep(2)
    else:
        print("❌ Mismatch in expected output. Exiting.")
        driver.quit()
        sys.exit(1)

# Appium options
options = UiAutomator2Options()
options.platform_name = 'Android'
options.platform_version = '12'
options.device_name = 'R9ZR601C18H'
options.automation_name = 'UiAutomator2'
options.app_package = 'com.android.phone'
options.app_activity = 'com.android.phone.DialtactsActivity'
options.no_reset = True
options.language = "en"
options.locale = "US"

# Initialize the driver
driver = webdriver.Remote(
    command_executor='http://localhost:4723',
    options=options
)

try:
    time.sleep(2)

    # Dial USSD code
    ussd_code = '*815' + '%23'
    driver.execute_script('mobile: shell', {
        'command': 'am',
        'args': ['start', '-a', 'android.intent.action.CALL', 'tel:' + ussd_code]
    })

    # USSD interaction flow
    send_input("1: Login", '1')                  # Step 1: Login
    send_input("Enter your PIN", '1992')      # Step 2: PIN
    send_input("2: Transfer", '2')            # Step 3: Choose transfer
    send_input("1: Transfer within BoA", '1') # Step 4: Internal transfer
    send_input("Enter Account No", '219783361')  # Step 5: Receiver account
    
    send_input("1: 219769865", '1')           # Step 6: Account type
    send_input("Enter Amount", '10')         # Step 7: Amount
    send_input("Enter Remark", 'test')        # Step 8: Remark
    send_input("1: Yes", '1')                 # Step 9: Confirm

    if wait_for_expected_output("complete", timeout=10):
        print("✅ Transaction complete. Now attempting to test the second Acc'...")

    send_input("complete", '*')      # Step 2: PIN
    send_input("2: Transfer", '2')            # Step 3: Choose transfer
    send_input("1: Transfer within BoA", '1') # Step 4: Internal transfer
    send_input("Enter Account No", '219769865')  # Step 5: Receiver account
    send_input("2: 219783361", '2')           # Step 6: Account type
    send_input("Enter Amount", '10')         # Step 7: Amount
    send_input("Enter Remark", 'test2')        # Step 8: Remark
    send_input("1: Yes", '1')                 # Step 9: Confirm


    # Final check for "complete" and press Cancel if found
    if wait_for_expected_output("complete", timeout=10):
        print("✅ Transaction complete. Now attempting to press 'Cancel'...")


        cancel_button_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancel")')
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(cancel_button_locator))
            cancel_button = driver.find_element(*cancel_button_locator)
            cancel_button.click()
            print("🛑 'Cancel' button clicked successfully.")
        except:
            print("⚠️ 'Cancel' button not found or not clickable.")
    else:
        print("❌ 'complete' message not found. Skipping cancel action.")

    print("\n✅ USSD Transaction flow completed.")

finally:
    driver.quit()
