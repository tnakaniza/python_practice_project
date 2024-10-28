from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class AccountPage:
    acc_select_dropdown_id = "accountSelect"
    deposit_btn_CSS_SELECTOR = "button[ng-click='deposit()']"
    amount_textbox_CSS_SELECTOR = "input[ng-model='amount']"
    submit_btn_CSS_SELECTOR = "button[type='submit']"
    balance_CSS_SELECTOR = "span[ng-bind='amount']"

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

        #wait = WebDriverWait(self.driver, 10)
        amount_textbox_CSS_SELECTOR_Element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.amount_textbox_CSS_SELECTOR)))
        amount_textbox_CSS_SELECTOR_Element.send_keys(amount)

        #wait = WebDriverWait(self.driver, 10)
        submit_btn_CSS_SELECTOR_Element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.submit_btn_CSS_SELECTOR)))
        submit_btn_CSS_SELECTOR_Element.click()

    def withdraw_amount(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "button[ng-click='withdrawl()']").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[ng-model='amount']").send_keys(amount)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_balance(self):
        wait = WebDriverWait(self.driver, 20)
        balance_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.balance_CSS_SELECTOR)))
        return int(balance_element.text)

    def open_transactions(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[ng-click='transactions()']").click()

    def validate_transaction(self, amount):
        transaction_table = self.driver.find_element(By.CSS_SELECTOR, "table")
        transactions = transaction_table.find_elements(By.TAG_NAME, "tr")
        for transaction in transactions:
            if str(amount) in transaction.text:
                return True
        return False

    def logout(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[ng-click='byebye()']").click()
