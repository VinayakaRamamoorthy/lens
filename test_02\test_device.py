import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config

class TestManageDevices(unittest.TestCase):

    def setUp(self):
        # Initialize WebDriver and page objects
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)

        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        # Quit WebDriver
        self.driver.quit()

    def test_login_and_manage_devices(self):
        # TC01: Launch Application
        # Step: Browser is launched and navigated to BASE_URL
        # Expected: Login page displayed (implicit by next step)

        # TC02: Login with Valid Credentials
        # Step: Enter valid USERNAME and PASSWORD, click Login
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # TC04: Handle Welcome Modal
        # Step: Check for welcome modal, close if present
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")

        # TC05: Navigate to Manage Section
        # Step: Click 'Manage'
        self.manage_page.open_manage()

        # TC06: Open Device Users Section
        # Step: Click 'Device Users'
        self.manage_page.open_device_users()

        # TC07: Wait for Devices to Load
        # Step: Wait for devices to load
        time.sleep(5)  # Replace with explicit wait if possible

        # TC08: Retrieve Connected Devices
        # Step: Retrieve devices
        devices = self.manage_page.get_all_devices()

        # TC09: Print Connected Devices
        # Step: Print devices
        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)

        # TC10: Validate Devices List Structure
        # Step: Validate list type
        self.assertIsInstance(devices, list, "Device list should be a list")

        # TC12: Empty Device List
        # Step: If no devices, "No devices found" message displayed
        if len(devices) == 0:
            # Already printed above, but could assert UI message if needed
            pass

        # TC13: Device Data Inconsistency
        # Step: Retrieve devices with missing/invalid fields
        # Placeholder: Implement functionality for device data inconsistency check

    def test_login_with_invalid_credentials(self):
        # TC03: Login with Invalid Credentials
        # Step: Enter invalid USERNAME or PASSWORD, click Login
        self.login_page.login("invalid_user", "invalid_pass")
        # Expected: Error message displayed, login fails
        # Placeholder: Implement assertion for error message on login failure

    def test_device_list_fails_to_load(self):
        # TC11: Device List Fails to Load
        # Step: Simulate device list API failure
        # Placeholder: Implement API failure simulation and assertion for error message

    def test_empty_device_list(self):
        # TC12: Empty Device List
        # Step: Wait for devices to load (none present)
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        time.sleep(5)
        devices = self.manage_page.get_all_devices()
        self.assertEqual(len(devices), 0, "Device list should be empty when no devices are connected")
        # Expected: "No devices found" message displayed

    def test_device_data_inconsistency(self):
        # TC13: Device Data Inconsistency
        # Step: Retrieve devices with missing/invalid fields
        # Placeholder: Implement functionality for device data inconsistency and assertion for error/warning

if __name__ == "__main__":
    unittest.main()
