Feature: Hotel price monitoring for optimal booking

  As a user planning a trip
  I want to know the date within the next 30 days when the price of a specific hotel is the lowest
  So that I can book the hotel at the optimal price

  Scenario Outline: Identify the date with the lowest hotel price within the next 30 days
    Given I am monitoring the price of the hotel "<hotel_name>" for the next 30 days
    When I analyze the prices for each day
    Then I should identify the date with the lowest price
    And notify me if that price is below "<desired_amount>"

    Examples:
      | hotel_name           | desired_amount |
      | The Charleston Place | 300            |
