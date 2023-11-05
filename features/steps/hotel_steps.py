import asyncio
import json

import aiohttp
import discord
from behave import *
from discord.webhook.async_ import AsyncWebhookAdapter, Webhook
from selenium import webdriver
from pages.HotelPage import HotelPage
from datetime import datetime, timedelta

from utilities.webdriver_extension import WebDriverExtension

use_step_matcher("re")


@given("I am monitoring the price of the hotel per night for \"(?P<hotel_name>.+)\" for the next 30 days")
def step_impl(context, hotel_name):
    context.hotel_name = hotel_name
    context.driver.get(
        "https://www.booking.com/")
    context.hotel_page = HotelPage(context.driver, hotel_name)
    context.ext = WebDriverExtension(context.driver)


@when("I analyze the prices for each day")
def step_impl(context):
    # Starting from tomorrow, up to 30 days in the future
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=30)

    context.min_price = float("inf")
    context.min_price_date = None

    current_date = start_date
    while current_date <= end_date:
        # Attempt to go to the next date and check the hotel name
        hotel_name_found = context.hotel_page.go_to_next_date(current_date, context.hotel_name)

        if hotel_name_found:
            price = context.hotel_page.get_price_for_date()  # Fetch price for the current date
            if price < context.min_price:
                context.min_price = price
                context.min_price_date = current_date

        # Increment the current date
        current_date += timedelta(days=1)


@then("I should identify the date with the lowest price")
def step_impl(context):
    assert context.min_price is not float("inf"), "No price was found."
    print(f"The lowest price found is {context.min_price} on {context.min_price_date.strftime('%Y-%m-%d')}")


@then("notify me if that price is below \"(?P<desired_amount>.+)\"")
def step_impl(context, desired_amount):
    desired_amount = float(desired_amount)
    if context.min_price < desired_amount:
        # Information for the Discord webhook
        webhook_url = 'https://discord.com/api/webhooks/1169126354453807105/Oe9ospsto73ai_H3CikklgWVeqfyF_W6dLlOFZuTLX2iljzmoh--_2TKx0_ydgx7gctm'

        # Form the message
        message = {
            "content": f"The lowest price for {context.hotel_name} found is {context.min_price} on "
                       f"{context.min_price_date.strftime('%Y-%m-%d')}, which is below your desired amount of {desired_amount}.",
            "username": "PriceNotifierBot"
        }

        # Run the asynchronous code using the event loop
        asyncio.run(send_discord_notification(webhook_url, message))


async def send_discord_notification(webhook_url, message):
    async with aiohttp.ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        try:
            response = await session.post(webhook_url, data=json.dumps(message), headers=headers)
            if response.status == 204:
                print("Message successfully sent to the Discord server.")
            else:
                print(f"Failed to send message to the Discord server. Response: {response.status}")
        except Exception as e:
            print(f"Failed to send message to the Discord server. Error: {e}")






