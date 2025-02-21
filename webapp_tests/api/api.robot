*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}        https://example.com
${BROWSER}    Chrome

*** Test Cases ***
Passing Test
    [Documentation]    This test will pass as the title is correctly matched.
    Open Browser    ${URL}    ${BROWSER}
    Title Should Be    Example Domain
    Close Browser

Failing Test
    [Documentation]    This test will fail as the title will not match.
    Open Browser    ${URL}    ${BROWSER}
    Title Should Be    Wrong Title
    Close Browser

