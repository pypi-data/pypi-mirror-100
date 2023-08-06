# robotframework-axelibrary

Robot Framework keyword library wrapper around [axe-selenium-python](https://github.com/mozilla-services/axe-selenium-python) library

## Installation:

 To install robotframework-axelibrary
 ```
 $ pip install robotframework-axelibrary
 ```

## Usage:

 ```
*** Settings ***
Library    SeleniumLibrary
Library    AxeLibrary

*** Test Cases ***
Google Accessibility Test
    Open Browser    https://www.google.com/    Chrome
    &{results}=    Run Accessibility Tests    google.json
    Log   Violations Count: ${results.violations}
    Get Json Accessibility Result
    Log Readable Accessibility Result    violations
    Log Readable Accessibility Result    incomplete
    [Teardown]    Close All Browsers
 ```

## Helpful Link to understand report

 - [Result Arrays](https://github.com/dequelabs/axe-core/blob/master/doc/API.md#result-arrays)