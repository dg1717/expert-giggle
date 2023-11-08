from datetime import datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.webdriver_extension import WebDriverExtension


def get_hotel_result_locator(hotel_name):
    return By.XPATH, f"(//div[contains(text(),'{hotel_name}')]/ancestor::div[@role='button'])[1]"


class HotelPage:
    # Class variables
    hotel_name_input = (By.CSS_SELECTOR, "[id=':re:']")
    date_selector = (By.CSS_SELECTOR, "[data-testid='date-display-field-start']")
    special_next_button = (By.XPATH, "//div[@class='next-button']//button")
    increment_date_locator = (By.XPATH,
                              "(//div[@aria-label='Start date']"
                              "//span[@aria-label='Increment date by one day'])[2]")
    search_button_locator = (By.CSS_SELECTOR, "button[type='submit']")
    clear_search = (By.CSS_SELECTOR, "[data-testid='input-clear']")
    price_display = (By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']")
    day_unavailable_message = (By.XPATH, "//p[contains(text(),'This property has no availability')]")
    hotel_name_locator = (By.XPATH, "(//body[@id='b2searchresultsPage']//div[@data-testid='title'])[1]")

    def __init__(self, driver, hotel_name):
        self.driver = driver
        self.hotel_name = hotel_name
        # Instance variables
        self.extension = WebDriverExtension(driver)
        self.enter_name_of_hotel(hotel_name)

    def get_price_for_date(self):
        price_element_text = self.extension.get_element_text(self.price_display)
        price = ''.join(filter(str.isdigit, price_element_text))
        return float(price)

    def enter_name_of_hotel(self, hotel):
        self.extension.find_and_send_keys(self.hotel_name_input, hotel)
        self.extension.find_and_click(get_hotel_result_locator(hotel))
        current_date = self.get_current_date_locator()
        self.extension.find_and_click(current_date)
        next_date = self.get_next_date_locator()
        self.extension.find_and_click(next_date)
        self.driver.save_screenshot('1_before_clicking_search.png')
        self.extension.find_and_click(self.search_button_locator)
        element = self.driver.find_element(*self.search_button_locator)
        element.click()
        self.driver.save_screenshot('2_after_clicking_search.png')
        self.get_price_for_date()

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
        self.extension.find_and_click(self.clear_search)
        self.extension.find_and_send_keys(self.hotel_name_input, hotel)
        self.extension.find_and_click(get_hotel_result_locator(hotel))
        # Click the calendar picker
        self.extension.find_and_click(self.date_selector)

        # Click the current date in the calendar picker
        current_date_locator = self.get_date_locator(current_date)
        self.extension.find_and_click(current_date_locator)

        # Click the search button to get the results for the incremented date
        self.extension.find_and_click(self.search_button_locator)

        # Wait for the site to load
        sleep(5)

        # Check if the hotel name matches
        hotel_name_text = self.extension.get_element_text(self.hotel_name_locator)

        if hotel_name_text is None or hotel.lower() not in hotel_name_text.lower():
            print(
                f"Hotel name '{hotel}' not found for date {current_date.strftime('%Y-%m-%d')}. Moving to the next date.")
            return False

        return True
