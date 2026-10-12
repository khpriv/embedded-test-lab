*** Settings ***
Library         embedded_test_lab.robot_library.EmbeddedDeviceLibrary
Resource        resources/device.resource
Suite Setup     Open Retrying Serial Device
Test Setup      Reset Device
Suite Teardown  Close Retrying Serial Device

Test Tags       retrying
Documentation   Retrying tests are for proof-of-concept demonstration. Exclude in regular test runs.


*** Variables ***
${DEFAULT_TEMPERATURE}  20
${DEFAULT_LIMIT}        80
${DEFAULT_STATUS}       READY


*** Test Cases ***
Hardware Default Temperature Is 20
    [Tags]  smoke
    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    ${DEFAULT_TEMPERATURE}


Hardware Temperature Can Be Changed
    [Tags]  smoke
    Set Temperature    40
    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    40


Hardware Default Limit Is 80
    [Tags]  smoke
    ${limit}=   Get Limit
    Should Be Equal As Integers     ${limit}   ${DEFAULT_LIMIT}


Hardware Default Status Is Ready
    [Tags]  smoke
    ${status}=  Get Status
    Should Be Equal As Strings      ${status}  ${DEFAULT_STATUS}


Hardware Limit Can Be Changed
    [Tags]  smoke
    Set Limit       100
    ${limit}=       Get Limit
    Should Be Equal As Integers     ${limit}    100


Hardware Status Can Be Changed
    [Tags]  smoke
    Set Status      INIT
    ${status}=      Get Status
    Should Be Equal As Strings      ${status}   INIT


Hardware Reset Restores Defaults
    [Tags]  smoke  regression
    Set Temperature     45
    Set Limit           120
    Set Status          NOT_READY
    Reset Device

    Device Should Be In Default State


Hardware Temperature Above Limit Is Rejected
    [Tags]  smoke  regression  negative

    Run Keyword And Expect Error
    ...  STARTS: ValueError:
    ...  Set Temperature    120

    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    ${DEFAULT_TEMPERATURE}