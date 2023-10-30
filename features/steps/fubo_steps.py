from behave import *
from pages.fubo_signup import FuboSignup
from utilities.driver_setup import WebDriverFactory


@when('I go to "{url}"')
@given('I go to "{url}"')
@then('I go to "{url}"')
def step_impl(context, url):
    context.driver = WebDriverFactory.get_webdriver("chrome")
    context.fubo_signup = FuboSignup(context.driver)
    context.driver.get(url)


@step("I click next")
def step_impl(context):
    context.fubo_signup.click_next()


@when("I create a new email and password")
def step_impl(context):
    context.fubo_signup.create_profile()


@when("I enter pay information")
def step_impl(context):
    print(context.fubo_signup.email)
    context.fubo_signup.enter_payment_info(context.home_page.card_number, context.home_page.card_exp, context.home_page.card_cvv)


@step("Click start free trial")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Click start free trial')


@step("Click Skip")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Click Skip')


@then("I should be on the profiles page")
def step_impl(context):
    context.driver.ext.wait_for_url_to_contain("/profiles")


@step("Click on new card")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Click on new card')


@step("Close the card")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And Close the card')


@then("I should see message that card has been closed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then I should see message that card has been closed')


@step("I click continue")
def step_impl(context):
    context.fubo_signup.click_continue()


@step("Pay monthly")
def step_impl(context):
    context.fubo_signup.pay_monthly()