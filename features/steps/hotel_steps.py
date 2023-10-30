from behave import *
from selenium import webdriver
from pages.HotelPage import HotelPage
from datetime import datetime, timedelta

from utilities.webdriver_extension import WebDriverExtension

use_step_matcher("re")


@given("I am monitoring the price of the hotel \"(?P<hotel_name>.+)\" for the next 30 days")
def step_impl(context, hotel_name):
    context.driver = webdriver.Chrome()
    context.driver.get(
        "https://kayak.com/hotels/")
    context.hotel_page = HotelPage(context.driver,hotel_name)
    context.ext = WebDriverExtension(context.driver)


@when("I analyze the prices for each day")
def step_impl(context):
    # Starting from tomorrow, up to 30 days in the future
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    context.ext.set_zoom_level(90)

    context.min_price = float("inf")
    context.min_price_date = None

    current_date = start_date
    while current_date <= end_date:
        price = context.hotel_page.get_price_for_date()  # Fetch price for the current date
        if price < context.min_price:
            context.min_price = price
            context.min_price_date = current_date

        # Move to the next date (e.g., by clicking a "next day" button or changing the date input)
        context.hotel_page.go_to_next_date()

        current_date += timedelta(days=1)


@then("I should identify the date with the lowest price")
def step_impl(context):
    assert context.min_price_date is not None, "Failed to identify the date with the lowest price"


@then("notify me if that price is below \"(?P<desired_amount>.+)\"")
def step_impl(context, desired_amount):
    if context.min_price < float(desired_amount):
        # Code to send an email or any other kind of notification
        pass  # Placeholder
    context.driver.quit()