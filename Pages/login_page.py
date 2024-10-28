from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    customer_login_btn_xpath = "//button[contains(.,'Customer Login')]"

    def __init__(self, driver):
        self.driver = driver

    def login_as_customer(self):
        wait = WebDriverWait(self.driver, 10)
        loginElement = wait.until(EC.visibility_of_element_located((By.XPATH, self.customer_login_btn_xpath)))
        loginElement.click()
