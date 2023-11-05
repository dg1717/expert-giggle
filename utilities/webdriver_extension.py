from time import sleep

from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WebDriverExtension:
    def __init__(self, driver):
        self.driver = driver

    def scroll_into_view(self, element):
        """Scrolls to make the element visible."""
        self.driver.execute_script("window.scrollTo(arguments[0].offsetLeft, arguments[0].offsetTop);", element)

    def find_and_send_keys(self, locator, value, retries=3):
        """Method to find an element using the provided locator and send keys to it with error handling and retries."""
        while retries:
            try:
                element = self.driver.find_element(*locator)  # This unpacks the tuple and finds the element
                self.scroll_into_view(element)
                element.clear()
                element.send_keys(value)
                return
            except (NoSuchElementException, ElementNotInteractableException):
                if retries == 1:  # if it's the last retry
                    raise
                retries -= 1
                sleep(1)  # wait for a second before retrying

    def find_and_click(self, locator, retries=3, wait_time=10):
        while retries:
            try:
                # Using WebDriverWait to ensure that the element is clickable before interacting with it.
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable(locator)
                )

                self.scroll_into_view(element)
                element.click()
                return

            except ElementClickInterceptedException:
                # If there's an obstruction, try scrolling the element into center view and then click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                sleep(1)  # Give a moment for any animations or changes to complete
                try:
                    element.click()  # Try to click again
                except ElementClickInterceptedException:
                    # Click with JavaScript as a fallback
                    self.driver.execute_script("arguments[0].click();", element)
                    return

            except (NoSuchElementException, ElementNotInteractableException):
                # Click with JavaScript as a fallback
                self.driver.execute_script("arguments[0].click();", element)
                return

            retries -= 1
            sleep(1)  # wait for a short duration before the next retry

        # If all retries have been exhausted, raise the exception.
        raise Exception(f"Failed to click the element with locator: {locator}")

    def wait_for_text_to_be_present(self, locator, text, timeout=2):
        try:
            element_present = EC.text_to_be_present_in_element(locator, text)
            WebDriverWait(self.driver, timeout).until(element_present)
            return True
        except TimeoutException:
            print(f"Timed out waiting for {locator} to have text: '{text}'")
            return False

    def open_new_tab(self, url=None):
        self.driver.execute_script("window.open('', '_blank');")

        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # If a URL is provided, navigate to it
        if url:
            self.driver.get(url)

    def get_element_text(self, locator, retries=3):
        while retries:
            try:
                element = self.driver.find_element(*locator)
                return element.text
            except (NoSuchElementException, ElementNotInteractableException):
                if retries == 1:  # if it's the last retry
                    raise

    def switch_to_previous_tab(self):
        """Switch to the other tab (assuming there are only two)."""
        # Get the current window handle
        current_window = self.driver.current_window_handle

        for handle in self.driver.window_handles:
            if handle != current_window:
                self.driver.switch_to.window(handle)
                break

    def wait_for_url_to_contain(self, substring, timeout=30):
        """
        Waits for the current URL to contain a specific substring.

        :param substring: The substring to check for in the current URL.
        :param timeout: How long to wait for the condition. Defaults to 30 seconds.
        """
        try:
            element_present = EC.url_contains(substring)
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print(f"Timed out waiting for URL to contain: {substring}")
            raise

    def set_zoom_level(self, zoom_level):
        params = {
            "width": 1280,
            "height": 800,
            "deviceScaleFactor": zoom_level / 100,
            "mobile": False
        }
        self.driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", params)
