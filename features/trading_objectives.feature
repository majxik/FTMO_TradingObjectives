Feature: Trading Objectives
  As a user interested in FTMO challenges
  I want to understand and verify the Trading Objectives section
  So that I can ensure the requirements are clear and testable

  Scenario: View Trading Objectives section
    Given I am on the FTMO homepage
    When I navigate to the "Trading Objectives" section
    Then I should see the list of trading objectives and their descriptions

  Scenario: Validate presence of key objectives
    Given I am on the Trading Objectives section
    Then I should see "Trading Period"
    And I should see "Minimum trading days"
    And I should see "Maximum Daily Loss"
    And I should see "Maximum Loss"
    And I should see "Profit Target"
    And I should see "Refundable Fee"

  Scenario: Check details for Maximum Daily Loss
    Given I am on the Trading Objectives section
    When I view the details for "Maximum Daily Loss"
    Then I should see an explanation of the daily loss limit

  Scenario: Check details for Profit Target
    Given I am on the Trading Objectives section
    When I view the details for "Profit Target"
    Then I should see an explanation of the profit target requirement

  Scenario: Validate presence of currency buttons
    Given I am on the Trading Objectives section
    Then I should see currency button "USD"
    And I should see currency button "GBP"
    And I should see currency button "EUR"
    And I should see currency button "CZK"
    And I should see currency button "CAD"
    And I should see currency button "AUD"
    And I should see currency button "CHF"

  Scenario: Validate presence of balance buttons for USD
    Given I am on the Trading Objectives section
    When I select currency "USD"
    Then I should see balance button "10 000 USD"
    And I should see balance button "25 000 USD"
    And I should see balance button "50 000 USD"
    And I should see balance button "100 000 USD"
    And I should see balance button "200 000 USD"

  Scenario: Validate Quick Comparison button
    Given I am on the Trading Objectives section
    Then I should see the "Quick Comparison" button

  Scenario: Validate default table values
    Given I am on the Trading Objectives section
    Then the table should contain "Trading Period"
    And the table should contain "Minimum trading days"
    And the table should contain "Maximum Daily Loss"
    And the table should contain "Maximum Loss"
    And the table should contain "Profit Target"
    And the table should contain "Refundable Fee"

  Scenario: Validate table values change with currency and balance
    Given I am on the Trading Objectives section
    When I select currency "EUR"
    And I select balance "50 000 EUR"
    Then the table should update values for selected currency and balance

  Scenario: Validate table values in Quick Comparison mode
    Given I am on the Trading Objectives section
    When I click the "Quick Comparison" button
    Then the comparison table should contain "Account Balance"
    And the comparison table should contain "Trading Period"
    And the comparison table should contain "Minimum Trading Days"
    And the comparison table should contain "Maximum Daily Loss"
    And the comparison table should contain "Maximum Loss"
    And the comparison table should contain "Profit Target"
    And the comparison table should contain "Refundable fee"

  Scenario: Validate details popup for table row
    Given I am on the Trading Objectives section
    When I click on table row "Maximum Daily Loss"
    Then I should see a popup with details and a YouTube video

  Scenario: Validate details popup is disabled in Quick Comparison mode
    Given I am on the Trading Objectives section
    When I click the "Quick Comparison" button
    Then table rows should not be clickable

  Scenario: Validate Start FTMO Challenge button
    Given I am on the Trading Objectives section
    Then I should see the "Start FTMO Challenge" button
    When I click the "Start FTMO Challenge" button
    Then I should be redirected to the login page
