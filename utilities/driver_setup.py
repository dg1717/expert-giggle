from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


class WebDriverFactory:

    @staticmethod
    def get_webdriver(browser_name="chrome", local_run=False):
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")

            if local_run:
                # Local execution
                return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            else:
                options.add_argument("--remote-debugging-port=9222")
                return webdriver.Chrome(options=options)


# Usage:
local_run = os.getenv('LOCAL_RUN', 'False').lower() in ('true', '1', 't')
driver = WebDriverFactory.get_webdriver(local_run=local_run)
