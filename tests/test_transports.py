import pytest
from embedded_test_lab.transports import SimulatorTransport


@pytest.mark.parametrize(
    "command, expected_response",
    [
        ("GET_TEMP", "TEMP:20"),
        ("GET_LIMIT", "LIMIT:80"),
        ("GET_STATUS", "STATUS:READY"),
        ("RESET", "OK"),
        ("SET_TEMP:25", "OK"),
        ("SET_LIMIT:100", "OK"),
        ("SET_STATUS:ERROR", "OK"),
        ("WRONG_COMM", "ERR:UNKNOWN_COMMAND"),
        ("SET_TEMP:150", "ERR:OUT_OF_RANGE"),
        ("SET_TEMP:SET_LIMIT:20", "ERR:INVALID_COMMAND"),
        ("SET_TEMP:apple", "ERR:INVALID_VALUE")
    ]
)
def test_simulatortransport(command, expected_response):
    transport = SimulatorTransport()
    assert transport.send(command) == expected_response


# new simulator has temperature 20
def test_default_temperature():
    transport = SimulatorTransport()
    assert transport.send("GET_TEMP") == "TEMP:20"


# setting temperature works
def test_temperature_can_be_changed():
    transport = SimulatorTransport()
    temperature = 40
    assert transport.send("GET_TEMP") == "TEMP:20"
    assert transport.send(f"SET_TEMP:{temperature}") == "OK"
    assert transport.send("GET_TEMP") == f"TEMP:{temperature}"


# too-high temperature is rejected
def test_temperature_over_limit_is_rejected():
    transport = SimulatorTransport()
    temperature = 100
    assert transport.send(f"SET_TEMP:{temperature}") == "ERR:OUT_OF_RANGE"


# rejected change preserves old state
def test_failed_temperature_change_doesnt_change_temperature():
    transport = SimulatorTransport()
    temperature = 100
    assert transport.send("GET_TEMP") == "TEMP:20"
    assert transport.send(f"SET_TEMP:{temperature}") == "ERR:OUT_OF_RANGE"
    assert transport.send("GET_TEMP") == "TEMP:20"


# unknown command returns error
def test_unknown_command():
    transport = SimulatorTransport()
    assert transport.send("INVALID_COMMAND") == "ERR:UNKNOWN_COMMAND"


# reset restores defaults
def test_reset_restores_defaults():
    transport = SimulatorTransport()

    temperature = 40
    assert transport.send(f"SET_TEMP:{temperature}") == "OK"
    assert transport.send("GET_TEMP") == f"TEMP:{temperature}"

    limit = 150
    assert transport.send(f"SET_LIMIT:{limit}") == "OK"
    assert transport.send("GET_LIMIT") == f"LIMIT:{limit}"

    status = "ERROR"
    assert transport.send(f"SET_STATUS:{status}") == "OK"
    assert transport.send("GET_STATUS") == f"STATUS:{status}"

    assert transport.send("RESET") == "OK"

    assert transport.send("GET_TEMP") == "TEMP:20"
    assert transport.send("GET_LIMIT") == "LIMIT:80"
    assert transport.send("GET_STATUS") == "STATUS:READY"


def test_temperature_can_be_set_after_limit_change():
    transport = SimulatorTransport()

    assert transport.send("SET_LIMIT:100") == "OK"
    assert transport.send("SET_TEMP:90") == "OK"
    assert transport.send("GET_TEMP") == "TEMP:90"


def test_temperature_invalid_value():
    transport = SimulatorTransport()

    assert transport.send("SET_TEMP:apple") == "ERR:INVALID_VALUE"


def test_limit_invalid_value():
    transport = SimulatorTransport()

    assert transport.send("SET_LIMIT:apple") == "ERR:INVALID_VALUE"


def test_invalid_command():
    transport = SimulatorTransport()

    assert transport.send("SET_LIMIT:SET_TEMP:20") == "ERR:INVALID_COMMAND"
