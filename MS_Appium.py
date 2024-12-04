import time
import unittest
from PIL import Image
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver as appium_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess


desired_cap = {
    "appium:uuid": f"emulator-5554",
    "platformName": "Android",
    "appium:deviceName": 'Android Emulator',
    "automationName": 'UiAutomator2',
    "appium:app": f"/Users/divyac/Documents/AppiumProject/Magic_studio/SampleAppv6Stage.apk"
}
appium_server_url = 'http://127.0.0.1:4723'
options = UiAutomator2Options().load_capabilities(desired_cap)


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url, options=options)
        print("Opening the app")
        time.sleep(5)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def list_files_in_download_folder(self):
        # Run the adb command to list files in the Downloads folder
        result = subprocess.run(['adb', 'shell', 'ls', '/sdcard/Download/'], capture_output=True, text=True)
        if result.returncode == 0:
            # Return a list of filenames
            return result.stdout.splitlines()
        else:
            print("Error listing files:", result.stderr)
            return []

    def find_and_click_file(self, filename):
        # Navigate to the Downloads folder in the app
        # This assumes you are already in the correct directory or using the file manager app
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Downloads")').click()

        # Wait for the file to be present and then click it
        file_element = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{filename}")'))
        )
        file_element.click()
        
    def test_scan(self):
        qrscanner = self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@content-desc="Scan QR"]').click()
        time.sleep(2)
        perm_while_using = self.driver.find_element(by=AppiumBy.XPATH, value='/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]').click()
        time.sleep(2)
        files = self.list_files_in_download_folder()

        # Example: Find and click the specific file "Amazon.png"
        if "Amazon.png" in files:
            self.find_and_click_file("Amazon.png")
        else:
            print("File 'Amazon.png' not found in the Downloads folder.")

        time.sleep(2)

if __name__ == '__main__':
    unittest.main()
