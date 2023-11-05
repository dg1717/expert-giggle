from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:

    @staticmethod
    def get_webdriver(browser_name="chrome"):
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Add any specific options for Chrome if required.
            # options.add_argument('--headless')
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

