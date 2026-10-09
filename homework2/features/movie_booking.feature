Feature: Movie theater booking

  As a movie theater customer
  I want to view movies and reserve available seats
  So that I can manage my movie bookings

  Scenario: View available movies
    Given a movie named "Interstellar" exists
    When I visit the movie list
    Then I should see "Interstellar"

  Scenario: Book an available seat
    Given a user named "student" exists
    And a movie named "Interstellar" exists
    And an available seat named "A1" exists
    And I am logged in as "student"
    When I book seat "A1" for "Interstellar"
    Then the booking should exist
    And seat "A1" should be marked booked

  Scenario: View booking history
    Given a user named "student" exists
    And a movie named "Interstellar" exists
    And an available seat named "A1" exists
    And "student" has booked seat "A1" for "Interstellar"
    And I am logged in as "student"
    When I visit my booking history
    Then I should see "Interstellar"
    And I should see seat "A1"