from behave import *
from pages.fubo_signup import FuboSignup
from utilities.driver_setup import WebDriverFactory


@given("I navigate to kayak site")
def step_impl(context):
    context.driver = WebDriverFactory.get_webdriver("chrome")
    context.fubo_signup = FuboSignup(context.driver)
    context.driver.get("https://www.kayak.com/")