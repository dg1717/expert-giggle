from behave import *
from pages.privacy_login_page import LoginPage
from pages.privacy_home_page import HomePage
from utilities.driver_setup import WebDriverFactory
from utilities.webdriver_extension import WebDriverExtension


@given('I navigate to login page')
def step_impl(context):
    context.driver = WebDriverFactory.get_webdriver("chrome")
    context.login_page = LoginPage(context.driver)
    context.home_page = HomePage(context.driver)
    context.driver.ext = WebDriverExtension(context.driver)
    context.login_page.open()


@when(u'I login')
def step_impl(context):
    context.login_page.fill_form("privacydg0104@email.ghostinspector.com", "Awesome0104.")


@then(u'I should see the home page')
def step_impl(context):
    context.driver.ext.wait_for_url_to_contain("/home")


@step("Do two factor authentication")
def step_impl(context):
    context.login_page.do_2fa()


@when("I create a new card")
def step_impl(context):
    context.home_page.create_card()
