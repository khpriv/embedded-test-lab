import pytest
from exercises import Device

def test_default_temperature():
    device = Device()
    assert device.get_temperature() == 20


def test_temperature_can_be_changed():
    device = Device()
    temperature = 40
    device.set_temperature(temperature)
    assert device.get_temperature() == temperature


def test_temperature_over_limit_raises_exception():
    device = Device()
    temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(temperature)

def test_failed_temperature_change_doesnt_change_temperature():
    device = Device()
    old_temperature = device.get_temperature()
    new_temperature = 100
    with pytest.raises(ValueError):
        device.set_temperature(new_temperature)
    assert device.get_temperature() == old_temperature


def test_reset_restores_defaults():
    device = Device()
    default_temperature = device.get_temperature()
    device.set_temperature(50)
    default_limit = device.get_limit()
    device.set_limit(150)
    default_status = device.get_status()
    device.set_status(0.5)
    device.reset()
    assert default_temperature == device.get_temperature()
    assert default_limit == device.get_limit()
    assert default_status == device.get_status()