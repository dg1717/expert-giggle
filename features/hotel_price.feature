Feature: Hotel price monitoring for optimal booking

  As a user planning a trip
  I want to know the date in a month when the price of a specific hotel is the lowest
  So that I can book the hotel at the optimal price

  @hotel @web
  Scenario Outline: [Web] Identify the date with the lowest price for The Charleston Place in a month
    Given I am monitoring the price of the hotel per night for "<hotel_name>" for the next 30 days
    When I analyze the prices for each day
    Then I should identify the date with the lowest price
    And notify me if that price is below "<desired_amount>"

    Examples:
      | hotel_name           | desired_amount |
      | The Charleston Place | 400            |

#  @hotel @mobile
#  Scenario Outline: [Mobile] Identify the date with the lowest price for The Charleston Place in a month
#    Given I am monitoring the price of the hotel per night for "<hotel_name>" for the next 30 days on my mobile device
#    When I analyze the prices for each day on the mobile app
#    Then I should identify the date with the lowest price
#    And notify me if that price is below "<desired_amount>" on my mobile device
#
#    Examples:
#      | hotel_name           | desired_amount |
#      | The Charleston Place | 400            |

