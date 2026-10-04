*** Settings ***
Library         embedded_test_lab.robot_library.EmbeddedDeviceLibrary
Resource        resources/device.resource
Suite Setup     Open Simulator Device
Test Setup      Reset Device
Suite Teardown  Close Device


*** Variables ***
${DEFAULT_TEMPERATURE}  20
${DEFAULT_LIMIT}        80
${DEFAULT_STATUS}       READY


*** Test Cases ***
Default Temperature Is 20
    [Tags]  smoke
    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    ${DEFAULT_TEMPERATURE}


Temperature Can Be Changed
    [Tags]  smoke
    Set Temperature    40
    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    40


Default Limit Is 80
    [Tags]  smoke
    ${limit}=   Get Limit
    Should Be Equal As Integers     ${limit}   ${DEFAULT_LIMIT}


Default Status Is Ready
    [Tags]  smoke
    ${status}=  Get Status
    Should Be Equal As Strings      ${status}  ${DEFAULT_STATUS}


Limit Can Be Changed
    [Tags]  smoke
    Set Limit       100
    ${limit}=       Get Limit
    Should Be Equal As Integers     ${limit}    100


Status Can Be Changed
    [Tags]  smoke
    Set Status      INIT
    ${status}=      Get Status
    Should Be Equal As Strings      ${status}   INIT


Reset Restores Defaults
    [Tags]  smoke  regression
    Set Temperature     45
    Set Limit           120
    Set Status          NOT_READY
    Reset Device

    Device Should Be In Default State


Temperature Above Limit Is Rejected
    [Tags]  smoke  regression  negative

    Run Keyword And Expect Error
    ...  STARTS: ValueError:
    ...  Set Temperature    120

    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    ${DEFAULT_TEMPERATURE}
