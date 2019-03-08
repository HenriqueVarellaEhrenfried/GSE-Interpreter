Feature: Allow student's request

Description:
    As a student
    I want to make a request
    So that I can improve my academic life

Group: Request

Constraints and Qualities:
    The requirement should implement:
    * A way to send requests to the course coordinator

Planning:
    This requirement will be implemented 6th and will take 6 hours to be implemented by 1 developer(s). The developer(s) responsible for implementing this requirement is/are Mariah Cash. The sprint that will implement this feature is: 3.

Scenario: Student request is successfully accepted
    Given that I am making a request 
    When I submit the request
    Then the system should display a success message
    And send the my request to the server   

Scenario: Student request is not accepted
    Given that I am making a request 
    When I submit the request
    Then the system should display a submit error message
    And do not send the request to the server 