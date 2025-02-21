*** Settings ***
Library    Collections
Library    OperatingSystem

*** Test Cases ***
Test Case 1 - Passing Test
    [Documentation]    This test should pass.
    Should Be Equal    10 + 10    1010

Test Case 2 - Another Passing Test
    [Documentation]    Another passing test.
    Should Contain    "Hello, Robot Framework Api!"    "Api"
