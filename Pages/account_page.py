import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class AccountPage:
    acc_select_dropdown_id = "accountSelect"
    deposit_btn_CSS_SELECTOR = "button[ng-click='deposit()']"
    amount_textbox_CSS_SELECTOR = "input[ng-model='amount']"
    submit_btn_CSS_SELECTOR = "button[type='submit']"
    balance_CSS_SELECTOR = "span[ng-bind='amount']"
    account_select_id = "accountSelect"
    options_tag_name = "option"

    def __init__(self, driver):
        self.driver = driver

    def select_account(self, account_number):
        wait = WebDriverWait(self.driver, 10)
        acc_select_dropdown_id_Element = wait.until(
            EC.visibility_of_element_located((By.ID, self.acc_select_dropdown_id)))
        acc_select_dropdown_id_Element.send_keys(account_number)
        print(f"Randomly selected acc: {account_number}")


    def deposit_amount(self, amount):
        wait = WebDriverWait(self.driver, 20)
        deposit_btn_CSS_SELECTOR_Element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.deposit_btn_CSS_SELECTOR)))
        deposit_btn_CSS_SELECTOR_Element.click()

        wait = WebDriverWait(self.driver, 20)
        amount_textbox_CSS_SELECTOR_Element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.amount_textbox_CSS_SELECTOR)))
        amount_textbox_CSS_SELECTOR_Element.send_keys(amount)

        wait = WebDriverWait(self.driver, 20)
        submit_btn_CSS_SELECTOR_Element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.submit_btn_CSS_SELECTOR)))
        submit_btn_CSS_SELECTOR_Element.click()

    def withdraw_amount(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "button[ng-click='withdrawl()']").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[ng-model='amount']").send_keys(amount)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_balance(self):
        wait = WebDriverWait(self.driver, 20)
        balance_element = wait.until(EC.visibility_of_element_located((By.XPATH, "(//strong[@class='ng-binding"
                                                                                        "'])[2]")))
        return int(balance_element.text)

    def open_transactions(self):
        #ToDO increase timer for test 3
        wait = WebDriverWait(self.driver, 20)
        trx_xpath_Element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Transactions')]")))
        trx_xpath_Element.click()

    def validate_transaction(self, amount):
        transaction_table = self.driver.find_element(By.CSS_SELECTOR, "table")
        transactions = transaction_table.find_elements(By.TAG_NAME, "tr")
        for transaction in transactions:
            if str(amount) in transaction.text:
                return True
        return False

    def logout(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[ng-click='byebye()']").click()

    def select_account_by_number(self, account_number):
        wait = WebDriverWait(self.driver, 20)
        try:
            # Wait until the specific account option is visible in the dropdown
            select_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//option[normalize-space(text())='{account_number}']"))
            )
            # Check if the element is interactable before clicking
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[normalize-space(text())='{account_number}']")))
            select_element.click()
            print(f"Successfully selected account: {account_number}")
        except TimeoutException:
            print(f"Could not find or select account number {account_number}")


        #select_element = self.driver.find_element(self.account_select)
        #select_element.find_element(By.XPATH, f"//option[. = '{account_number}']").click()


    def get_all_account_numbers(self):
        try:
            # Wait for the dropdown to be visible
            wait = WebDriverWait(self.driver, 10)
            dropdown_element = wait.until(EC.visibility_of_element_located((By.ID, self.acc_select_dropdown_id)))

            # Create a Select object to interact with the dropdown
            select = Select(dropdown_element)

            # Get all options in the dropdown and extract their text
            account_numbers = [option.text for option in select.options if option.text.strip()]
            print("Account numbers found:", account_numbers)

            return account_numbers

        except Exception as e:
            print(f"Error in get_all_account_numbers: {e}")
            return []

    def get_first_account_number(self):
        wait = WebDriverWait(self.driver, 10)
        options_tag_name_Element = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, self.options_tag_name[0])))


        #select_element = self.driver.find_element(self.account_select)
        first_option = options_tag_name_Element.find_elements(By.TAG_NAME, "option")[0]
        return first_option.text
