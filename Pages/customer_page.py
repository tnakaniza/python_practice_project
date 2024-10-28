import random

from selenium.webdriver.chrome import options
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class CustomerPage:
    dropdown_id = "userSelect"
    login_btn_xpath = "//button[contains(.,'Login')]"
    account_select = (By.ID, "accountSelect")
    logout_btn = (By.CSS_SELECTOR, "button[ng-click='byebye()']")

    def __init__(self, driver):
        self.driver = driver

    def select_random_customer(self):
        wait = WebDriverWait(self.driver, 10)
        dropdown_id_Element = wait.until(EC.visibility_of_element_located((By.ID, self.dropdown_id)))

        # Locate the dropdown
        select_element = Select(dropdown_id_Element)

        # Get all options from the dropdown
        options = select_element.options

        # Select a random option, excluding the first option if it's a placeholder
        random_index = random.randint(1, len(options) - 1)  # start from 1 to skip placeholder if needed
        select_element.select_by_index(random_index)
        # Get the selected customer name for logging purposes (optional)
        selected_customer = options[random_index].text
        print(f"Randomly selected customer: {selected_customer}")

        # Click the Login button
        wait = WebDriverWait(self.driver, 10)
        customer_login_btn_Element = wait.until(EC.visibility_of_element_located((By.XPATH, self.login_btn_xpath)))
        customer_login_btn_Element.click()

    def get_all_account_numbers(self):
        select_element = self.driver.find_element(self.account_select)
        options = select_element.find_elements(By.TAG_NAME, "option")
        return [option.text for option in options]

    def select_account_by_number(self, account_number):
        select_element = self.driver.find_element(self.account_select)
        select_element.find_element(By.XPATH, f"//option[. = '{account_number}']").click()