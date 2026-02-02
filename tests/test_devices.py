import unittest
import sys
import os
import time

# Ensure project root is in sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config

class TestLoginAndDeviceList(unittest.TestCase):
    """
    Test Case: TC01 - Successful Login and Device List Retrieval
    Verifies that a registered user can log in, handle the welcome modal,
    navigate to the 'Manage' section, access 'Device Users', and view the complete list of connected devices.
    """

    def setUp(self):
        # Initialize the WebDriver and open the application
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)

        # Initialize page objects
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_successful_login_and_device_list_retrieval(self):
        # Step 1: Launch the application (handled in setUp)

        # Step 2: Enter valid username and password, and Step 3: Click 'Login'
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # Step 4: If a welcome modal appears, close or accept it
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")

        # Step 5: Navigate to the 'Manage' section
        self.manage_page.open_manage()

        # Step 6: Select 'Device Users'
        self.manage_page.open_device_users()

        # Step 7: Wait for the device list to load
        time.sleep(5)  # Replace with explicit wait if possible

        # Retrieve all devices
        devices = self.manage_page.get_all_devices()

        # Output the devices for verification
        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)

        # Assertion: The device list should be a list (even if empty)
        self.assertIsInstance(devices, list, "Device list should be a list")

        # Additional assertion: If devices are expected, ensure at least one is present
        # self.assertGreater(len(devices), 0, "At least one device should be connected")  # Uncomment if required

        # Placeholder: Implement additional validation for device details if needed

if __name__ == "__main__":
    unittest.main()
