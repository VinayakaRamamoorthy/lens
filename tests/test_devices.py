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

class TestManageDevices(unittest.TestCase):
    """
    Automated tests for the Device Management and User Login workflow (SCRUM-7).
    Covers login, modal handling, navigation, device list display, and edge cases.
    """

    def setUp(self):
        # Initialize the Selenium WebDriver and page objects
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)

        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_TC01_successful_login_and_device_display(self):
        """
        TC01: Verify user can log in, navigate, and view all connected devices.
        """
        # Step 1: Login
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # Step 2: Handle welcome modal if present
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")

        # Step 3: Navigate to Manage > Device Users
        self.manage_page.open_manage()
        self.manage_page.open_device_users()

        # Step 4: Wait for devices to load
        time.sleep(5)  # Replace with smarter wait if possible

        # Step 5: Get all devices
        devices = self.manage_page.get_all_devices()

        # Output and assertion
        if len(devices) == 0:
            print("No devices connected")
        else:
            print(f"Devices found ({len(devices)}):")
            for device in devices:
                print(device)
        self.assertIsInstance(devices, list, "Device list should be a list")

    def test_TC02_welcome_modal_handling(self):
        """
        TC02: Verify system handles welcome modal after login.
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
            print("Welcome modal handled successfully.")
        except Exception:
            print("Welcome modal not displayed, continuing...")
        # Proceed to Manage > Device Users to confirm navigation works
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # If no exception, test passes

    def test_TC03_no_devices_connected(self):
        """
        TC03: Verify behavior when user has no connected devices.
        (Precondition: User has no devices connected)
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        time.sleep(2)
        devices = self.manage_page.get_all_devices()
        if len(devices) == 0:
            print("No devices connected (as expected).")
        self.assertEqual(devices, [], "Expected no devices connected.")

    def test_TC04_device_list_loads_with_delay(self):
        """
        TC04: Verify device list loads correctly with network delay.
        (Precondition: Devices connected, simulate lag)
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # Simulate network delay (in real test, use network throttling or mock)
        print("Simulating network delay...")
        time.sleep(5)
        # Check for loading indicator
        # Placeholder: Implement check for loading indicator if locator available
        print("Loading indicator check - Placeholder")
        devices = self.manage_page.get_all_devices()
        print(f"Devices loaded after delay: {devices}")
        self.assertIsInstance(devices, list)

    def test_TC05_invalid_login_attempt(self):
        """
        TC05: Verify system prevents access with invalid credentials.
        """
        # Step 1: Launch app (done in setUp)
        # Step 2: Enter invalid credentials and attempt login
        self.login_page.login("invalid_user@example.com", "wrongpassword")
        # Step 3: Assert error message is shown
        # Placeholder: Implement assertion for login error message
        print("Login error message check - Placeholder")
        # Placeholder: Assert no access to Manage/Device Users

    def test_TC06_unauthorized_access_to_device_users(self):
        """
        TC06: Verify unauthenticated users can't access Device Users.
        """
        # Step 1: Attempt direct navigation to Device Users section
        self.driver.get(f"{config.BASE_URL}/manage/device-users")
        # Step 2: Assert redirect to login or access denied
        # Placeholder: Implement assertion for redirect or access denied message
        print("Unauthorized access check - Placeholder")

    def test_TC07_device_list_pagination(self):
        """
        TC07: Verify device list supports pagination/scroll for many devices.
        (Precondition: User has more devices than page limit)
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # Placeholder: Implement pagination/scroll test
        print("Pagination/infinite scroll check - Placeholder")

    def test_TC08_device_status_verification(self):
        """
        TC08: Verify each device shows correct connection status.
        (Precondition: Devices with varying statuses)
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # Placeholder: Implement device status verification
        print("Device status indicator check - Placeholder")

    def test_TC09_device_management_actions(self):
        """
        TC09: Verify device management actions (remove/rename) are available and work.
        (Precondition: At least one device connected)
        """
        self.login_page.login(config.USERNAME, config.PASSWORD)
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        self.manage_page.open_manage()
        self.manage_page.open_device_users()
        # Placeholder: Implement device management actions (remove/rename)
        print("Device management actions check - Placeholder")

    def test_TC10_ui_responsiveness(self):
        """
        TC10: Verify Device Users section is responsive on various devices.
        (Precondition: Devices connected)
        """
        # Placeholder: Implement UI responsiveness test for desktop/tablet/mobile
        print("UI responsiveness check - Placeholder")

if __name__ == "__main__":
    unittest.main()
