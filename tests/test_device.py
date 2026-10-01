import pytest
from exercises import Device
from transports import SimulatorTransport, FakeTransport

def test_default_temperature():
    device = Device(SimulatorTransport())
    assert device.get_temperature() == 20


def test_temperature_can_be_changed():
    device = Device(SimulatorTransport())
    temperature = 40
    device.set_temperature(temperature)
    assert device.get_temperature() == temperature


def test_temperature_over_limit_raises_exception():
    device = Device(SimulatorTransport())
    temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(temperature)

def test_failed_temperature_change_doesnt_change_temperature():
    device = Device(SimulatorTransport())
    old_temperature = device.get_temperature()
    new_temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(new_temperature)
    assert device.get_temperature() == old_temperature


def test_reset_restores_defaults():
    device = Device(SimulatorTransport())

    device.set_temperature(50)
    device.set_limit(150)
    device.set_status("ERROR")

    device.reset()

    assert device.get_temperature() == 20
    assert device.get_limit() == 80
    assert device.get_status() == "READY"


def test_get_temperature():
    transport = FakeTransport("TEMP:25")
    device = Device(transport)

    assert device.get_temperature() == 25

# GET_TEMP causes Device to send exactly "GET_TEMP"
def test_faketransport_invalid_response_for_get_temp():
    device = Device(FakeTransport("GET_TEMP"))
    with pytest.raises(RuntimeError):
        device.get_temperature()


# "STATUS:READY" returned for GET_TEMP raises RuntimeError
def test_faketransport_returns_status():
    device = Device(FakeTransport("STATUS:READY"))
    with pytest.raises(RuntimeError):
        device.get_temperature()

# "banana" or another malformed response raises an error
def test_faketransport_returns_banana():
    device = Device(FakeTransport("banana"))
    with pytest.raises(RuntimeError):
        device.set_temperature(25)


def test_get_temperature_sends_correct_command():
    transport = FakeTransport("TEMP:25")
    device = Device(transport)

    device.get_temperature()

    assert transport.last_command == "GET_TEMP"
