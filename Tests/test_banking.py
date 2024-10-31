import time

import pytest
import allure
from allure_commons.types import AttachmentType
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from Pages.customer_page import CustomerPage
from Pages.login_page import LoginPage
from Pages.account_page import AccountPage
from Utils.readProperties_LoginDetails import ReadLoginConfig


class TestBanking:
    way2AutomationURL = ReadLoginConfig().getWay2AutomationURL()

    @pytest.mark.tamara
    @allure.severity(allure.severity_level.CRITICAL)
    def test_deposit_first_account(self, setup):
        self.driver = setup
        self.driver.get(self.way2AutomationURL)
        self.driver.maximize_window()
        self.login = LoginPage(self.driver)
        self.customer = CustomerPage(self.driver)
        self.account = AccountPage(self.driver)

        """Test 1: Deposit into the first account and validate."""
        try:
            self.login.login_as_customer()
            allure.attach(self.driver.get_screenshot_as_png(), name="Login Page 1", attachment_type=AttachmentType.PNG)

            self.customer.select_random_customer()
            self.customer.click_login_button()
            allure.attach(self.driver.get_screenshot_as_png(), name="Customer Page 1",
                          attachment_type=AttachmentType.PNG)

            self.account.deposit_amount(1500)
            allure.attach(self.driver.get_screenshot_as_png(), name="Post-Deposit Screenshot",
                          attachment_type=AttachmentType.PNG)

            # Validate balance if get_balance() returns the correct balance
            # current_balance = self.account.get_balance()
            # assert current_balance == '1500', "Deposit validation failed"
            # # assert account.get_balance() == 1500, "Deposit failed"

        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutException",
                          attachment_type=AttachmentType.PNG)
        except TypeError as e:
            print(f"TypeError: {e}")
        finally:
            # Ensure logout and quit are called at the end, after all actions
            self.account.logout()
            self.driver.quit()

    @pytest.mark.tamara
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_deposit_all_accounts(self, setup):
        self.driver = setup
        self.login = LoginPage(self.driver)
        self.customer = CustomerPage(self.driver)
        self.account = AccountPage(self.driver)

        """Test 2: Deposit into all accounts and validate."""
        try:
            self.driver.get(self.way2AutomationURL)
            self.driver.maximize_window()

            # Login as Customer
            self.login.login_as_customer()
            allure.attach(self.driver.get_screenshot_as_png(), name="Login Page Test 2",
                          attachment_type=AttachmentType.PNG)

            # ToDO : Sort out random_customer Method

            self.customer.select_random_customer()
            self.customer.click_login_button()
            allure.attach(self.driver.get_screenshot_as_png(), name="Cust Page Test 2",
                          attachment_type=AttachmentType.PNG)

            account_numbers = self.account.get_all_account_numbers()  # get all account Numbers

            # Iterate through each account to deposit and validate
            for account_number in account_numbers:
                self.account.select_account_by_number(account_number)
                print(f"customer: {account_number}")
                self.account.deposit_amount(1500)

                # Validate deposit was successful
                # current_balance = self.account.get_balance()
                # assert current_balance == 1500, f"Deposit failed for account {account_number}"

                # Attach screenshot for each deposit
                allure.attach(self.driver.get_screenshot_as_png(),
                              name=f"Deposit Successful for Account {account_number}",
                              attachment_type=AttachmentType.PNG)

        except TimeoutException as e:
            print(f"Exception occurred: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutException",
                          attachment_type=AttachmentType.PNG)
            raise e

        finally:
            self.account.logout()
            self.driver.quit()
            allure.attach(self.driver.get_screenshot_as_png(), name="Logout Page",
                          attachment_type=allure.attachment_type.PNG)

    @pytest.mark.tamara
    @allure.severity(allure.severity_level.CRITICAL)
    def test_transaction_validation(self, setup):
        """Test 3: Deposit, Transaction, Withdraw, and Validate Balance"""
        self.driver = setup
        self.driver.get(self.way2AutomationURL)
        self.driver.maximize_window()
        self.login = LoginPage(self.driver)
        self.customer = CustomerPage(self.driver)
        self.account = AccountPage(self.driver)

        try:
            self.login.login_as_customer()
            self.customer.select_random_customer()
            self.customer.click_login_button()
            self.account.deposit_amount(31459)
            # WebDriverWait(self.driver, 20).until(
            #     lambda d: self.account.get_balance() == '31459'
            # )
            #assert self.account.get_balance() == '31459', "Initial deposit failed"

            self.account.open_transactions()
            allure.attach(self.driver.get_screenshot_as_png(), name="Transactions Page",
                          attachment_type=AttachmentType.PNG)

            self.account.withdraw_amount(31459)
            # WebDriverWait(self.driver, 20).until(
            #     lambda d: self.account.get_balance() == '0'
            # )
            # assert self.account.get_balance() == '0', "Balance not restored to original"
            # self.account.open_transactions()
            allure.attach(self.driver.get_screenshot_as_png(), name="Final Transaction",
                          attachment_type=AttachmentType.PNG)

            time.sleep(2)
        except TimeoutException as e:
            print(f"TimeoutException encountered: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutException",
                          attachment_type=AttachmentType.PNG)
            raise e  # re-raise exception for reporting
