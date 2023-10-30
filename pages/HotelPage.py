from time import sleep

from selenium.webdriver.common.by import By

from utilities.webdriver_extension import WebDriverExtension


class HotelPage:

    def __init__(self, driver, hotel_name):
        self.driver = driver
        self.extension = WebDriverExtension(driver)
        self.enter_name_of_hotel(hotel_name)

    hotel_name_input = (By.XPATH, "//input[contains(@placeholder,'Enter a city,')]")
    date_selector = (By.XPATH, "//input[contains(@placeholder,'Enter a city,')]")
    special_next_button = (By.XPATH, "//div[@class='next-button']//button")
    increment_date_locator = (By.XPATH,
                              "(//div[@aria-label='Start date']"
                              "//span[@aria-label='Increment date by one day'])[2]")
    search_button_locator = (By.XPATH, "//button[@aria-label='Search']")
    price_display = (By.XPATH,
                     "(//div[@class='kzGk kzGk-mod-flexible-height'])[1]//div[@data-target='price']")

    def set_date(self, date):
        self.extension.find_and_send_keys(self.date_selector, date)

    def get_price_for_date(self):
        price_element_text = self.extension.get_element_text(self.price_display)

        # Assuming the price is displayed as '$100' or '100 USD', we need to extract only the numeric value
        price = ''.join(filter(str.isdigit, price_element_text))
        return float(price) / 100  # converting cents to dollar format

    def enter_name_of_hotel(self, hotel):
        self.extension.find_and_send_keys(self.hotel_name_input, hotel)
        self.extension.find_and_click(self.search_button_locator)

    def go_to_next_date(self):
        # Click to increment the date
        self.extension.find_and_click(self.increment_date_locator)

        # Click the search button to get the results for the incremented date
        self.extension.find_and_click(self.search_button_locator)

        # Wait for site to load
        sleep(5)


