import asyncio
from datetime import datetime, timedelta, time
from time import sleep

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.webdriver_extension import WebDriverExtension


def get_hotel_result_locator(hotel_name):
    return By.XPATH, f"(//div[contains(text(),'{hotel_name}')]/ancestor::div[@role='button'])[1]"


class HotelPage:
    # Class variables
    hotel_name_input = (By.CSS_SELECTOR, "[id=':re:']")
    date_selector = (By.CSS_SELECTOR, "[data-testid='date-display-field-start']")
    search_button_locator = (By.CSS_SELECTOR, "button[type='submit']")
    clear_search = (By.CSS_SELECTOR, "[data-testid='input-clear']")
    close_google_popup_button = (By.CSS_SELECTOR, "[id='close']")
    price_display = (By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']")
    close_sign_in_button = (By.CSS_SELECTOR, "[aria-label='Dismiss sign-in info.']")
    day_unavailable_message = (By.XPATH, "//p[contains(text(),'This property has no availability')]")
    hotel_name_locator = (By.XPATH, "(//body[@id='b2searchresultsPage']//div[@data-testid='title'])[1]")

    def __init__(self, driver, hotel_name):
        self.driver = driver
        actions = ActionChains(self.driver)
        self.hotel_name = hotel_name
        # Instance variables
        self.extension = WebDriverExtension(driver)
        self.enter_name_of_hotel(hotel_name)

    def get_price_for_date(self):
        price_element_text = self.extension.get_element_text(self.price_display)
        price = ''.join(filter(str.isdigit, price_element_text))
        return float(price)

    def enter_name_of_hotel(self, hotel):
        print(type(self.driver.name))
        self.close_sign_in()
        if self.driver.name.lower() not in ['chrome', 'msedge']:
            self.close_google_popup()
        self.extension.find_and_send_keys(self.hotel_name_input, hotel)
        self.extension.find_and_click(get_hotel_result_locator(hotel))
        current_date = self.get_current_date_locator()
        self.extension.find_and_click(current_date)
        next_date = self.get_next_date_locator()
        self.extension.find_and_click(next_date)
        self.extension.find_and_click(self.search_button_locator)
        element = self.driver.find_element(*self.search_button_locator)
        self.extension.find_and_click(element)
        self.get_price_for_date()

    def close_google_popup(self):
        iframe_locator = (By.CSS_SELECTOR, "[title='Sign in with Google Dialog']")
        iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(iframe_locator))

        # Switch to the iframe
        self.driver.switch_to.frame(iframe)
        self.extension.click_with_js(self.close_google_popup_button)
        self.driver.switch_to.default_content()

    def close_sign_in(self):
        try:
            # Add a sleep for 3 seconds
            sleep(3)

            # Check if the close button element is present
            close_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Dismiss sign-in info.']")

            # If the element is present, execute the script
            close_button_script = "document.querySelector(\"[aria-label='Dismiss sign-in info.']\").click();"
            self.driver.execute_script(close_button_script)
        except NoSuchElementException:
            # Handle the case when the element is not present
            print("Close button not found. Skipping script execution or adding alternative logic.")

    @staticmethod
    def get_date_locator(date):
        # Format the given date in the required 'YYYY-MM-DD' format
        date_str = date.strftime('%Y-%m-%d')

        # Return the locator for the given date as a tuple
        return By.CSS_SELECTOR, f"[data-date='{date_str}']"

    @staticmethod
    def get_current_date_locator():
        # Get the current date
        current_date = datetime.now()

        # Format the current date in the required 'YYYY-MM-DD' format
        current_date_str = current_date.strftime('%Y-%m-%d')

        # Return the locator for the current date as a tuple
        return By.CSS_SELECTOR, f"[data-date='{current_date_str}']"

    @staticmethod
    def get_next_date_locator():
        # Get the current date
        current_date = datetime.now()

        # Add one day to the current date to get the next date
        next_date = current_date + timedelta(days=1)

        # Format the next date in the required 'YYYY-MM-DD' format
        next_date_str = next_date.strftime('%Y-%m-%d')

        # Return the locator for the next date as a tuple
        return By.CSS_SELECTOR, f"[data-date='{next_date_str}']"

    def go_to_next_date(self, current_date, hotel):
        self.extension.click_with_js(self.clear_search)
        self.extension.find_and_send_keys(self.hotel_name_input, hotel)
        self.extension.click_with_js(get_hotel_result_locator(hotel))
        # Click the calendar picker
        self.extension.click_with_js(self.date_selector)

        # Select the check-in/checkout dates the calendar picker
        current_date_locator = self.get_date_locator(current_date)
        checkout_date = current_date + timedelta(days=1)
        checkout_date_locator = self.get_date_locator(checkout_date)
        self.extension.find_and_click(current_date_locator)
        self.extension.find_and_click(checkout_date_locator)

        # Click the search button to get the results for the incremented date
        self.extension.find_and_click(self.search_button_locator)

        # Wait for the site to load
        sleep(4)

        # Check if the hotel name matches
        hotel_name_text = self.extension.get_element_text(self.hotel_name_locator)

        if hotel_name_text is None or hotel.lower() not in hotel_name_text.lower():
            print(
                f"Hotel name '{hotel}' not found for date {current_date.strftime('%Y-%m-%d')}. Moving to the next date.")
            return False

        return True
