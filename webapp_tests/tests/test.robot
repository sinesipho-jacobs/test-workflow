*** Settings ***
Library    Collections
Library    OperatingSystem

*** Test Cases ***
Test Case 1 - Passing Test
     [Documentation]    This test should pass.
     Should Be Equal    2 + 2    4

# Test Case 2 - Another Passing Test
#     [Documentation]    Another passing test.
#     Should Contain    "Hello, Robot Framework!"    "Robot"

 Test Case 3 - Failing Test
     [Documentation]    This test should fail.
     Should Be Equal    5 * 2    15

# Test Case 4 - Conditional Test
#    [Documentation]    Test with IF condition.
#    ${value}    Set Variable    10
#    Run Keyword If    ${value} == 10    Log    ✅ Condition Met
#    Run Keyword If    ${value} != 10    Fail    ❌ Condition Failed

# Test Case 5 - Skipped Test
#     [Documentation]    Example of a skipped test.
#     [Tags]    skip
#     Log    🚧 This test is skipped.
