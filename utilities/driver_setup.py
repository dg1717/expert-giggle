from selenium import webdriver


class WebDriverFactory:

    @staticmethod
    def get_webdriver(browser_name="chrome"):
        """
        Initialize and return the webdriver instance based on the browser_name provided.

        :param browser_name: Name of the browser. Default is "chrome".
        :return: WebDriver instance.
        """
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Add any specific options for Chrome if required.
            # options.add_argument('--headless')
            return webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            # Add any specific options for Firefox if required.
            return webdriver.Firefox(options=options)

        # Similarly, you can add conditions for other browsers like Edge, Safari, etc.

        raise Exception(f"Browser '{browser_name}' is not supported.")
