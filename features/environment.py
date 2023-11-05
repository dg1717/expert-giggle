from utilities.driver_setup import WebDriverFactory


def before_scenario(context, scenario):
    # Initialize the WebDriver before each scenario
    # Choose the method based on the value of isRemote
    if WebDriverFactory.isRemote:
        context.driver = WebDriverFactory.get_remote_webdriver()
    else:
        context.driver = WebDriverFactory.get_webdriver()


def after_scenario(context, scenario):
    # Quit the WebDriver after each scenario
    if hasattr(context, "driver"):
        context.driver.quit()


def after_step(context, step):
    if step.status == "failed":
        # Take a screenshot or perform some other error handling/logging
        # Ensure that the directory for the screenshots exists or handle the FileNotFoundError
        context.driver.save_screenshot(f"screenshots/{step.name}.png")
