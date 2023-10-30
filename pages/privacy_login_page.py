from selenium.webdriver.common.by import By
from utilities.webdriver_extension import WebDriverExtension


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.ext = WebDriverExtension(driver)  # Initialize WebDriverExtension
        self.email_input = (By.CSS_SELECTOR, "[name='email']")
        self.password_input = (By.CSS_SELECTOR, "[name='password']")
        self.login_button = (By.CSS_SELECTOR, "[data-test='button-login']")
        self.access_code = (By.CSS_SELECTOR, "[name='token']")
        self.two_fa_email = (By.XPATH, "//a[text()='New Device Login']/..")
        self.two_fa_code_we = (By.CSS_SELECTOR, "p[class='authentication-code']")
        self.login_button_2fa = (By.CSS_SELECTOR,"button[type='button']")
        self.two_fa_code = None

    def open(self):
        self.driver.get("https://app.privacy.com/login")

    def fill_form(self, email, password):
        self.ext.find_and_send_keys(self.email_input, email)
        self.ext.find_and_send_keys(self.password_input, password)  # Fixed from email_input to password_input
        self.ext.find_and_click(self.login_button)

    def do_2fa(self):
        self.ext.open_new_tab("https://email.ghostinspector.com/privacydg0104")
        self.ext.find_and_click(self.two_fa_email)
        self.two_fa_code = self.ext.get_element_text(self.two_fa_code_we)
        self.ext.switch_to_previous_tab()
        self.ext.find_and_send_keys(self.access_code,self.two_fa_code)
        self.ext.find_and_click(self.login_button_2fa)



