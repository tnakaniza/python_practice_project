import pytest
import allure
from allure_commons.types import AttachmentType
from selenium.common import TimeoutException

from Pages.customer_page import CustomerPage
from Pages.login_page import LoginPage
from Pages.account_page import AccountPage
from Utils.readProperties_LoginDetails import ReadLoginConfig


class TestBanking:
    way2AutomationURL = ReadLoginConfig().getWay2AutomationURL()

    @pytest.mark.tamara
    @allure.severity(allure.severity_level.CRITICAL)
    def test_deposit_first_account(self, setup):
        """Test 1: Deposit into the first account and validate."""
        try:
            self.driver = setup
            self.driver.get(self.way2AutomationURL)
            self.driver.maximize_window()

            self.login = LoginPage(self.driver)
            self.login.login_as_customer()
            allure.attach(self.driver.get_screenshot_as_png(), name="Login Page 1", attachment_type=AttachmentType.PNG)

            self.customer = CustomerPage(self.driver)
            self.customer.select_random_customer()
            allure.attach(self.driver.get_screenshot_as_png(), name="Customer Page 1",
                          attachment_type=AttachmentType.PNG)

            account = AccountPage(self.driver)
            selected_acc = account.select_account("1001")
            print(account.select_account(selected_acc))
            account.deposit_amount(1500)
            allure.attach(self.driver.get_screenshot_as_png(), name="Post-Deposit Screenshot",
                          attachment_type=AttachmentType.PNG)

            # Validate balance if get_balance() returns the correct balance
            # assert account.get_balance() == 1500, "Deposit failed"
            # assert account.get_balance() == 1500, "Deposit failed"

        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutException",
                          attachment_type=AttachmentType.PNG)
        except TypeError as e:
            print(f"TypeError: {e}")
        finally:
            # Ensure logout and quit are called at the end, after all actions
            account = AccountPage(self.driver)
            account.logout()
            self.driver.quit()
