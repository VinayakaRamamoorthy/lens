import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
import config

# Placeholder: Import AccountPage if available
# from pages.account_page import AccountPage

class TestGuestUserLoginButton(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.driver.get(config.BASE_URL)
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        # Placeholder: Initialize AccountPage if available
        # self.account_page = AccountPage(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def navigate_to_account_section(self):
        """
        Helper to navigate to the account section.
        Placeholder: Implement navigation to account section if AccountPage is available.
        """
        # Placeholder: Implement navigation to account section
        # self.account_page.open_account_section()
        # For now, try to click an 'Account' link or button if present
        try:
            account_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'account') or contains(text(), 'Account')]")
            )
            account_link.click()
        except TimeoutException:
            print("Account section link/button not found. Please implement navigation.")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", account_link)

    def get_login_button(self):
        """
        Helper to get the Login button element in the account section.
        """
        try:
            login_btn = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//button[text()='LOG IN' or text()='Login']"))
            )
            return login_btn
        except TimeoutException:
            return None

    def test_TC01_login_button_visible_to_guest_user(self):
        """
        TC01: Ensure guest user sees Login button in account section
        """
        print("\n[TC01] Checking Login button visibility for guest user...")
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible to guest user.")

    def test_TC02_login_button_hidden_for_authenticated_user(self):
        """
        TC02: Ensure authenticated user does not see Login button
        """
        print("\n[TC02] Checking Login button is hidden for authenticated user...")
        # Login
        self.login_page.login(config.USERNAME, config.PASSWORD)
        # Handle welcome modal if present
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed, continuing...")
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNone(login_btn, "Login button should NOT be visible to authenticated user.")

    def test_TC03_login_button_redirects_to_login_page(self):
        """
        TC03: Clicking Login button as guest redirects to login page
        """
        print("\n[TC03] Checking Login button redirects to login page...")
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible to guest user.")
        try:
            login_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", login_btn)
        # Placeholder: Assert user is redirected to login page (check URL or login form)
        self.assertTrue(
            "login" in self.driver.current_url.lower() or
            self.wait.until(EC.visibility_of_element_located(LoginPage.EMAIL)),
            "User should be redirected to login page."
        )

    def test_TC04_login_button_accessible_via_keyboard(self):
        """
        TC04: Login button can be focused and activated with keyboard
        """
        print("\n[TC04] Checking keyboard accessibility of Login button...")
        self.navigate_to_account_section()
        # Tab to Login button
        body = self.driver.find_element(By.TAG_NAME, "body")
        found = False
        for _ in range(10):  # Tab up to 10 times
            body.send_keys(Keys.TAB)
            focused = self.driver.switch_to.active_element
            if focused == self.get_login_button():
                found = True
                break
        self.assertTrue(found, "Login button should be focusable via keyboard.")
        # Press Enter to activate
        focused.send_keys(Keys.ENTER)
        # Placeholder: Assert activation (e.g., redirection or login form appears)
        self.assertTrue(
            "login" in self.driver.current_url.lower() or
            self.wait.until(EC.visibility_of_element_located(LoginPage.EMAIL)),
            "Login button should be activated by keyboard."
        )

    def test_TC05_login_button_visible_on_all_browsers_devices(self):
        """
        TC05: Login button visible on all supported browsers/devices
        """
        print("\n[TC05] Checking Login button visibility on all browsers/devices...")
        # Placeholder: Implement cross-browser/device test in CI or with parameterization
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible on all browsers/devices.")

    def test_TC06_graceful_handling_of_network_failure(self):
        """
        TC06: System handles network failure when loading account section
        """
        print("\n[TC06] Checking graceful handling of network failure...")
        # Placeholder: Simulate network failure (e.g., using browser devtools or proxy)
        # self.driver.set_network_conditions(offline=True)  # Not supported in Selenium directly
        # For now, just a placeholder
        print("Placeholder: Simulate network failure and check for error message or fallback UI.")
        # Placeholder: Assert error message or fallback UI is shown

    def test_TC07_multiple_rapid_clicks_on_login_button(self):
        """
        TC07: System handles multiple rapid clicks on Login button gracefully
        """
        print("\n[TC07] Checking multiple rapid clicks on Login button...")
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible to guest user.")
        for _ in range(5):
            try:
                login_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", login_btn)
            time.sleep(0.1)
        # Placeholder: Assert no crash, no duplicate redirects (e.g., check only one navigation)
        print("Placeholder: Verify only one redirect occurred and no crash.")

    def test_TC08_login_button_visible_after_session_expiry(self):
        """
        TC08: Login button appears after guest session expires
        """
        print("\n[TC08] Checking Login button visibility after session expiry...")
        # Placeholder: Expire session (e.g., delete cookies)
        self.driver.delete_all_cookies()
        self.driver.refresh()
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible after session expiry.")

    def test_TC09_login_button_visible_with_js_disabled(self):
        """
        TC09: Login button visible or fallback provided if JS is disabled
        """
        print("\n[TC09] Checking Login button visibility with JS disabled...")
        # Placeholder: Relaunch browser with JS disabled (not supported in Selenium directly)
        print("Placeholder: Relaunch browser with JS disabled and check for Login button or fallback.")
        # Placeholder: Assert Login button or fallback is visible

    def test_TC10_login_button_announced_by_screen_reader(self):
        """
        TC10: Login button is accessible and announced by screen reader
        """
        print("\n[TC10] Checking screen reader accessibility of Login button...")
        self.navigate_to_account_section()
        login_btn = self.get_login_button()
        self.assertIsNotNone(login_btn, "Login button should be visible to guest user.")
        # Placeholder: Use accessibility API or axe-core to check ARIA label/role
        print("Placeholder: Verify Login button is announced by screen reader (ARIA label/role).")

if __name__ == "__main__":
    unittest.main()
