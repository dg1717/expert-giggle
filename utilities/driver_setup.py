import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:
    isRemote = 'true'

    @staticmethod
    def get_webdriver(browser_name="chrome"):
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('window-size=1920x1080')
            # options.add_argument('--headless')  # Corrected argument
            # options.add_argument('--disable-gpu')  # Recommended to avoid unnecessary use of GPU
            # options.add_argument('--enable-logging')
            # options.add_argument('--v=1')
            # options.add_argument('--no-sandbox')
            # options.add_argument(
            #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
            # options.add_argument('--disable-dev-shm-usage')
            # options.page_load_strategy = 'normal'

            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
