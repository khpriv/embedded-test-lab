*** Settings ***
Library         embedded_test_lab.robot_library.EmbeddedDeviceLibrary
Resource        resources/device.resource
Suite Setup     Open Serial Device
Test Setup      Reset Device
Suite Teardown  Close Serial Device
Test Tags       hardware faultinjection


*** Variables ***
${DEFAULT_TEMPERATURE}  20
${DEFAULT_LIMIT}        80
${DEFAULT_STATUS}       READY


*** Test Cases ***
Hardware Timeout Error When Response Delayed
    [Tags]  negative
    FIT Set Response Delay  FIT_DELAY:500

    Run Keyword And Expect Error
    ...  STARTS: TimeoutError:
    ...  Set Temperature    50

    Recover After FIT