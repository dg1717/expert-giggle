import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:
    isRemote = True

    @staticmethod
    def get_webdriver(browser_name="chrome"):
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Add any specific options for Chrome if required.
            # options.add_argument('--headless')
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    @staticmethod
    def get_remote_webdriver(browser_name="chrome"):

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Add any specific options for Chrome if required.
            # If running in GitHub Actions (or any remote environment), run headless
            if WebDriverFactory.isRemote:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
            # Setup ChromeDriver
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
