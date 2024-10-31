import random
from venv import logger

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class CustomerPage:
    user_select_id = "userSelect"
    login_btn_xpath = "//button[contains(.,'Login')]"
    account_select_xpath = "//select[@id='accountSelect']"
    options_tag_name = "option"

    def __init__(self, driver):
        self.driver = driver

    def select_random_customer(self):
        wait = WebDriverWait(self.driver, 30)
        dropdown_id_Element = wait.until(EC.visibility_of_element_located((By.ID, self.user_select_id)))

        # Locate the dropdown
        #select_element = self.driver.find_element(By.ID, self.user_select_id)

        # Get all options from the dropdown
        options = dropdown_id_Element.find_elements(By.TAG_NAME, "option")

        # Select a random option, excluding any placeholder or empty option
        options = [option for option in options if option.text.strip()]
        random_option = random.choice(options)

        # Click the randomly selected option
        random_option.click()
        print(f"Randomly selected customer: {random_option.text}")

        return random_option.text

        # Click the Login button
    def click_login_button(self):
        wait = WebDriverWait(self.driver, 20)
        customer_login_btn_Element = wait.until(EC.visibility_of_element_located((By.XPATH, self.login_btn_xpath)))
        customer_login_btn_Element.click()