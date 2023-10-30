import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.webdriver_extension import WebDriverExtension


class FuboSignup:
    def __init__(self, driver):
        self.driver = driver
        self.ext = WebDriverExtension(driver)
        self.next_button = (By.CSS_SELECTOR, "button[title='Next']")
        self.email_input = (By.CSS_SELECTOR, "[data-testid='sign-up-email-fld']")
        self.password_input = (By.CSS_SELECTOR, "[data-testid='sign-up-password-fld']")
        self.zip_input = (By.CSS_SELECTOR, "[name='homePostalCode']")
        self.confirm_zip_input = (By.CSS_SELECTOR, "[data-testid='sign-up-zip-confirm-btn']")
        self.continue_button = (By.CSS_SELECTOR, "[data-testid='sign-up-continue-btn']")
        self.premier_button = (By.CSS_SELECTOR, "[data-testid='premier-fubo-basic-v2-selection-button']")
        self.package_continue_button = (By.CSS_SELECTOR, "[data-testid='package-page-continue-button']")
        self.first_card_name = (By.CSS_SELECTOR, "[data-testid='sign-up-cc-first-name-fld']")
        self.last_card_name = (By.CSS_SELECTOR, "[data-testid='sign-up-cc-last-name-fld']")
        self.cc_num_field = (By.CSS_SELECTOR, "[id='recurly-hosted-field-input']")
        self.cc_exp_field = (By.CSS_SELECTOR, "[title='MM / YY']")
        self.cc_cvv_field = (By.CSS_SELECTOR, "[title='CVV']")
        self.pay_monthly_button = (By.CSS_SELECTOR, "[value='pro-fubo-basic-v2']")
        self.pay_monthly_button_two = (By.XPATH, "(//button[@data-button-type='primary'])[1]")
        self.cc_zip_field = (By.CSS_SELECTOR, "[name='postal_code']")
        self.special_next_button = (By.XPATH, "//div[@class='next-button']//button")
        self.submit_payment_btn = (By.CSS_SELECTOR, "[data-testid='sign-up-payment-submit-right-button']")
        self.email = self.generate_random_email("fuboman", "email.ghostinspector.com")
        self.password = "Awesome0104."
        self.zip = "29579"

    def click_next(self):
        self.ext.find_and_click(self.next_button)

    def create_profile(self):
        self.ext.find_and_send_keys(self.email_input,self.email)
        self.ext.find_and_send_keys(self.password_input,self.password)
        self.ext.find_and_send_keys(self.zip_input,self.zip)
        self.ext.find_and_click(self.confirm_zip_input)
        self.ext.find_and_click(self.continue_button)

    def click_continue(self):
        self.ext.find_and_click(self.package_continue_button)

    def enter_payment_info(self, card_number, card_exp, card_cvv):
        try:
            # Wait for the iframe to be available and switch to it by title
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="Billing information"]'))
            )
        except Exception as e:
            # Handle exceptions (e.g., iframe not found)
            print("Failed to switch to the iframe:", str(e))
        self.ext.find_and_send_keys(self.cc_num_field, card_number)
        self.ext.find_and_send_keys(self.cc_exp_field, card_exp)
        self.ext.find_and_send_keys(self.cc_cvv_field, card_cvv)
        self.driver.switch_to.default_content()

    def start_free_trial(self):
        self.ext.find_and_click(self.submit_payment_btn)

    def pay_monthly(self):
        try:
            # Check if element1 is present and displayed
            WebDriverWait(self.driver, 10).until(EC.visibility_of(
                self.driver.find_element(By.CSS_SELECTOR, "[value='pro-fubo-basic-v2']")))

            # If element1 is present and displayed, click it
            self.ext.find_and_click(self.pay_monthly_button)
        except Exception as e:
            # If element1 is not present or not displayed, click element2
            self.ext.find_and_click(self.pay_monthly_button_two)

        self.ext.find_and_click(self.special_next_button)

    @staticmethod
    def generate_random_email(base_email, domain):
        """
            Generate a random email based on a base email and domain.

            :param base_email: The base email name (everything before the '+' sign).
            :param domain: The email's domain.
            :return: A new email string with a random 5-digit number.
            """
        # Generate a random 5-digit number
        random_number = random.randint(10000, 99999)

        # Create the first part of the email up to (and including) the '+' sign
        email_prefix = f"{base_email}+{random_number}"

        # Combine the parts to create the full email address
        full_email = f"{email_prefix}@{domain}"

        return full_email
