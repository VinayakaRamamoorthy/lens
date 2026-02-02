import unittest
import sys
import os
import time

# Ensure project root is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage  # Placeholder: Implement WelcomeModalPage if missing
from pages.manage_page import ManagePage
import config

class TestLoginAndDeviceManagementFlow(unittest.TestCase):
    """
    Implements the workflow:
    - Login to application
    - Handle welcome modal
    - Navigate to Manage > Device Users
    - Retrieve and print connected devices
    - Validate device list
    - Handles edge/negative cases (invalid login, empty device list, device list load failure)
    """

    def setUp(self):
        # Step TC01: Launch browser and navigate to BASE_URL
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)

        # Initialize page objects
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)  # Placeholder: Ensure WelcomeModalPage is implemented
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login_and_device_management(self):
        # TC02: Login with Valid Credentials
        # Step: Enter valid USERNAME and PASSWORD, Click Login
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # TC04/TC05: Handle Welcome Modal (if present)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")

        # TC06: Navigate to Manage Section
        self.manage_page.open_manage()

        # TC07: Open Device Users Section
        self.manage_page.open_device_users()

        # TC08: Wait for Devices to Load
        time.sleep(5)  # Replace with explicit wait if possible

        # TC09: Retrieve Connected Devices
        devices = self.manage_page.get_all_devices()

        # TC10: Print Connected Devices
        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)

        # TC11: Validate Devices List
        self.assertIsInstance(devices, list, "Device list should be a list")

    def test_login_with_invalid_credentials(self):
        # TC03: Login with Invalid Credentials
        # Step: Enter invalid USERNAME or PASSWORD, Click Login
        self.login_page.login("invalid_user", "invalid_pass")
        # Placeholder: Implement error message locator and assertion
        # Example:
        # error_msg = self.driver.find_element(By.XPATH, "//div[@class='error']")
        # self.assertTrue(error_msg.is_displayed())
        print("Placeholder: Validate error message for invalid login")

    def test_device_list_fails_to_load(self):
        # TC12: Device List Fails to Load
        # Simulate device list load failure
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # Placeholder: Simulate device list load failure (e.g., network disconnect, API mock)
        # Placeholder: Assert error message and retry option
        print("Placeholder: Simulate device list load failure and validate error handling")

    def test_empty_device_list(self):
        # TC13: Empty Device List
        # Step: Wait for devices, expect "No devices connected" message
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        time.sleep(5)
        devices = self.manage_page.get_all_devices()
        if len(devices) == 0:
            print("No devices connected")
            # Placeholder: Assert "No devices connected" message is displayed
            # Example:
            # msg = self.driver.find_element(By.XPATH, "//h4[normalize-space()='No Device Users']")
            # self.assertTrue(msg.is_displayed())
        else:
            print("Devices found when none expected:", devices)
        self.assertEqual(devices, [], "Device list should be empty when no devices are connected")

if __name__ == "__main__":
    unittest.main()
