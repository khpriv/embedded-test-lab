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
Temperature Above Changed Limit Is Rejected Try Except
    [Tags]   regression   negative
    ${new_temperature}=     Set Variable    60
    ${limit}=               Set Variable    50

    Set Limit               ${limit}

    TRY
        Set Temperature    ${new_temperature}
    EXCEPT    ValueError:    type=START    AS    ${error}
        Log    Expected rejection: ${error}
    ELSE
        Fail    Setting temperature above limit did not raise ValueError
    END

    ${temperature}=    Get Temperature
    Should Be Equal As Integers    ${temperature}    ${DEFAULT_TEMPERATURE}