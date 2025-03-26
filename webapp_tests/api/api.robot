*** Settings ***
Library    Collections
Library    OperatingSystem

*** Test Cases ***
Test Case 1
    Sleep    3

# Test Case 2 - Another Passing Test
#     [Documentation]    Another passing test.
#     Should Contain    "Hello, Robot Framework Api!"    "Api"
Test Case 2
    [Documentation]    Another passing test.
    Sleep    3

