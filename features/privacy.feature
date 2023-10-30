Feature: Logging in to privacy

  Scenario: Login to privacy and make an account at fubo
    Given I navigate to login page
    When I login
    And Do two factor authentication
    Then I should see the home page
    When I create a new card
    Given I go to "https://www.fubo.tv/signup"
    And I click next
    When I create a new email and password
    And I click next
    And I click continue
    And Pay monthly
    And I click next
    When I enter pay information
    And Click start free trial
    And Click Skip
    Then I should be on the profiles page


  Scenario: Fubo sign up
    Given I go to "https://www.fubo.tv/signup"
    And I click next
    When I create a new email and password
    And I click next
    And I click continue
    And Pay monthly
    When I enter pay information
    And Click start free trial
    And Click Skip
    Then I should be on the profiles page
    When I go to "https://app.privacy.com/home"
    And Click on new card
    And Close the card
    Then I should see message that card has been closed