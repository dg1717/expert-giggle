from utilities.driver_setup import WebDriverFactory
from utilities.appium_setup import AppiumSetup


def before_scenario(context, scenario):
    if "web" in scenario.tags:
        # Initialize the WebDriver for web scenarios
        context.driver = WebDriverFactory.get_webdriver()
    elif "mobile" in scenario.tags:
        # Initialize the Appium driver for mobile scenarios
        context.appium_setup = AppiumSetup(platform_version="14.0")
        context.appium_setup.start_driver()
        context.driver = context.appium_setup.driver


def after_scenario(context, scenario):
    # Quit the appropriate driver after each scenario
    if hasattr(context, "driver"):
        context.driver.quit()
    if "mobile" in scenario.tags and hasattr(context, "appium_setup"):
        context.appium_setup.stop_driver()


def after_step(context, step):
    if step.status == "failed":
        # Handle screenshot taking for both web and mobile
        # Ensure the appropriate directory for screenshots exists
        context.driver.save_screenshot(f"screenshots/{step.name}.png")
