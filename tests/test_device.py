import pytest
from unittest.mock import Mock
from embedded_test_lab.device import Device, DeviceProtocolError
from embedded_test_lab.transports import (SimulatorTransport, SerialTransport, FakeTransport, RetryingTransport, FlakyTransport)
import logging


@pytest.fixture
def device():
    transport = SimulatorTransport()
    device = Device(transport)

    yield device


@pytest.fixture
def device_teardown():
    transport = SimulatorTransport()
    device = Device(transport)

    print("SETUP")
    yield device
    print("TEARDOWN")


def test_default_temperature(device):
    assert device.get_temperature() == 20


def test_temperature_can_be_changed(device):
    temperature = 40
    device.set_temperature(temperature)
    assert device.get_temperature() == temperature


def test_temperature_over_limit_raises_exception(device):
    temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(temperature)


def test_failed_temperature_change_doesnt_change_temperature(device):
    old_temperature = device.get_temperature()
    new_temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(new_temperature)
    assert device.get_temperature() == old_temperature


def test_reset_restores_defaults(device):
    device.set_temperature(50)
    device.set_limit(150)
    device.set_status("ERROR")

    device.reset()

    assert device.get_temperature() == 20
    assert device.get_limit() == 80
    assert device.get_status() == "READY"


def test_get_temperature():
    device = Device(FakeTransport("TEMP:25"))

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


def test_faketransport_returns_banana():
    device = Device(FakeTransport("banana"))
    with pytest.raises(RuntimeError):
        device.set_temperature(25)


def test_get_temperature_sends_correct_command():
    transport = FakeTransport("TEMP:25")
    device = Device(transport)
    device.get_temperature()
    assert transport.last_command == "GET_TEMP"


def test_get_temperature_sends_correct_command_via_mock():
    transport = Mock()
    transport.send.return_value = "TEMP:25"
    device = Device(transport)

    assert device.get_temperature() == 25
    transport.send.assert_called_once_with("GET_TEMP")


def test_get_temperature_rejects_wrong_response_type():
    transport = Mock()
    transport.send.return_value = "STATUS:READY"
    device = Device(transport)

    with pytest.raises(DeviceProtocolError):
        device.get_temperature()
    transport.send.assert_called_once_with("GET_TEMP")


def test_temperature_can_be_changed_via_mock():
    transport = Mock()
    transport.send.return_value = "OK"
    device = Device(transport)

    device.set_temperature(25)
    transport.send.assert_called_once_with("SET_TEMP:25")


def test_temperature_over_limit_raises_exception_via_mock():
    transport = Mock()
    transport.send.return_value = "ERR:OUT_OF_RANGE"
    device = Device(transport)
    temperature = 100

    with pytest.raises(ValueError):
        device.set_temperature(temperature)
    transport.send.assert_called_once_with("SET_TEMP:100")


def test_default_temperature_retrying_transport_4th_attempt():
    flaky = FlakyTransport(SimulatorTransport(), 3)
    retrying = RetryingTransport(flaky)
    device = Device(retrying)

    assert device.get_temperature() == 20
    assert flaky.calls == 4


def test_default_temperature_retrying_transport_3rd_attempt_via_mock(caplog):
    caplog.set_level(logging.WARNING)
    underlying = Mock()
    underlying.send.side_effect = [TimeoutError(),
                                   TimeoutError(),
                                   "TEMP:20"]
    sleeper = Mock()

    transport = RetryingTransport(underlying, retries=3, retry_delay=0.5, sleeper=sleeper)

    assert transport.send("GET_TEMP") == "TEMP:20"
    assert underlying.send.call_count == 3
    sleeper.assert_called_with(0.5)
    assert sleeper.call_count == 2
    assert "Timeout" in caplog.text
    assert any(
        record.levelno == logging.WARNING
        for record in caplog.records
    )


def test_default_temperature_retrying_transport_immediate_response():
    flaky = FlakyTransport(SimulatorTransport(), 0)
    retrying = RetryingTransport(flaky)
    device = Device(retrying)

    assert device.get_temperature() == 20
    assert flaky.calls == 1


def test_timeout_after_all_retries():
    flaky = FlakyTransport(SimulatorTransport(), 100)
    retrying = RetryingTransport(flaky)
    device = Device(retrying)

    with pytest.raises(TimeoutError):
        device.get_temperature()
    assert flaky.calls == 4


def test_timeout_after_all_retries_via_mock(caplog):
    caplog.set_level(logging.WARNING)
    retries = 4
    underlying = Mock()
    underlying.send.side_effect = TimeoutError()
    sleeper = Mock()

    transport = RetryingTransport(underlying, retries=retries, retry_delay=0.5, sleeper=sleeper)

    with pytest.raises(TimeoutError):
        transport.send("GET_TEMP")
    assert underlying.send.call_count == retries + 1
    sleeper.assert_called_with(0.5)
    assert sleeper.call_count == retries
    assert any(
        record.levelno == logging.WARNING
        for record in caplog.records
    )
    assert any(
        record.levelno == logging.ERROR
        for record in caplog.records
    )

@pytest.mark.hardware
def test_basic_device_smoke():
    with SerialTransport("/dev/ttyACM0") as transport:
        device = Device(transport)

        device.reset()

        assert device.get_temperature() == 20
        assert device.get_limit() == 80
        assert device.get_status() == "READY"

        device.set_temperature(40)
        assert device.get_temperature() == 40

        device.set_limit(60)
        assert device.get_limit() == 60

        device.set_status("TESTING")
        assert device.get_status() == "TESTING"

        device.reset()

        assert device.get_temperature() == 20
        assert device.get_limit() == 80
        assert device.get_status() == "READY"
