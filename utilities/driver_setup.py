import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from shutil import which
import logging
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import EdgeOptions

from utilities.config_reader import ConfigReader


class WebDriverFactory:
    isRemote = 'true'

    @staticmethod
    def get_webdriver():
        config_reader = ConfigReader()
        browser_name = config_reader.get_browser_option('BROWSER', 'Name', fallback='chrome')

        if browser_name == "chrome":
            driver = WebDriverFactory.get_chrome_driver(config_reader)
        elif browser_name == "edge":
            driver = WebDriverFactory.get_edge_driver(config_reader)
        elif browser_name == "firefox":
            driver = WebDriverFactory.get_firefox_driver(config_reader)
        elif browser_name == "safari":
            driver = WebDriverFactory.get_safari_driver(config_reader)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        WebDriverFactory.clear_cookies(driver)

        return driver

    @staticmethod
    def get_chrome_driver(config_reader):
        options = webdriver.ChromeOptions()
        WebDriverFactory.set_common_options(options, config_reader)
        # Add any Chrome-specific options here
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    @staticmethod
    def get_edge_driver(config_reader):
        driver = webdriver.Edge()
        return driver

    @staticmethod
    def get_firefox_driver(config_reader):
        options = webdriver.FirefoxOptions()
        WebDriverFactory.set_common_options(options, config_reader)
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    @staticmethod
    def get_safari_driver(config_reader):
        options = webdriver.SafariOptions()

        # Create Safari WebDriver
        driver = webdriver.Safari(options=options)

        # Maximize the window using JavaScript
        driver.execute_script(
            "window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);")

        return driver

    @staticmethod
    def clear_cookies(driver):
        """
        Clear cookies for the given WebDriver instance.

        :param driver: WebDriver instance
        """
        if isinstance(driver, webdriver.Safari):
            # For Safari, use JavaScript to clear cookies
            driver.execute_script(
                "document.cookie.split(';').forEach(function(c) { document.cookie = c.replace(/^\\s+/,'').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/'); });")
        else:
            # For other browsers, use delete_all_cookies
            driver.delete_all_cookies()

    @staticmethod
    def set_common_options(options, config_reader):
        window_size = config_reader.get_common_option('WindowSize')
        options.add_argument(window_size)

        is_remote = config_reader.get_common_option('IsRemote', fallback='false')
        if is_remote.lower() == 'true':
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_experimental_option(
        #     "prefs", {
        #         # block image loading
        #         "profile.managed_default_content_settings.images": 2,
        #     }
        # )
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-web-security')
        options.add_argument('--enable-logging')
        options.add_argument('--v=1')
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        options.page_load_strategy = 'eager'
