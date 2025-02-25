*** Settings ***
Library    Collections
Library    OperatingSystem

*** Test Cases ***
Test Case 1 - Passing Test
    [Documentation]    This test should pass.
    Should Be Equal    2 + 2    4

