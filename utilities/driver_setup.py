import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:
    isRemote = os.getenv('GITHUB_ACTIONS') == 'true'

    @staticmethod
    def get_webdriver(browser_name="chrome"):
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Add any specific options for Chrome if required.

            if WebDriverFactory.isRemote:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')

            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Usage
driver = WebDriverFactory.get_webdriver()
