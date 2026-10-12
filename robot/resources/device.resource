*** Settings ***
Library         embedded_test_lab.robot_library.EmbeddedDeviceLibrary

*** Variables ***
${DEFAULT_TEMPERATURE}  20
${DEFAULT_LIMIT}        80
${DEFAULT_STATUS}       READY


*** Keywords ***
Device Should Be In Default State
    [Documentation]    Verifies that temperature, limit and status match DUT defaults.
    ${temperature}=     Get Temperature
    ${limit}=           Get Limit
    ${status}=          Get Status
    Should Be Equal As Integers     ${temperature}  ${DEFAULT_TEMPERATURE}
    Should Be Equal As Integers     ${limit}        ${DEFAULT_LIMIT}
    Should Be Equal As Strings      ${status}       ${DEFAULT_STATUS}



Recover After FIT
    Run Keyword And Ignore Error
    ...    Reset Device

    Sleep  1s
    Clear Input Buffer
