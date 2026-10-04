from robot.api.deco import keyword, library
from robot.api import logger as robot_logger

from embedded_test_lab.device import Device
from embedded_test_lab.transports import SimulatorTransport


@library(scope="SUITE")
class EmbeddedDeviceLibrary:

    def __init__(self) -> None:
        self.device: Device | None = None

    def _get_device(self) -> Device:
        if self.device is None:
            raise RuntimeError("Device is not open")

        return self.device

    @keyword("Open Simulator Device")
    def open_simulator_device(self) -> None:
        """Open transport to simulated DUT"""
        robot_logger.info("Open transport to simulated DUT")
        self.device = Device(SimulatorTransport())

    @keyword("Close Device")
    def open_device(self) -> None:
        """Close transport to device"""
        self.device = None

    @keyword("Get Temperature")
    def get_temperature(self) -> int:
        """Get temperature of simulated DUT"""
        return self._get_device().get_temperature()

    @keyword("Set Temperature")
    def set_temperature(self, temperature: int) -> None:
        """Set temperature of simulated DUT"""
        self._get_device().set_temperature(temperature)

    @keyword("Get Status")
    def get_status(self) -> str:
        """Get status of simulated DUT"""
        return self._get_device().get_status()

    @keyword("Set Status")
    def set_status(self, status: str) -> None:
        """Set status of simulated DUT"""
        self._get_device().set_status(status)

    @keyword("Get Limit")
    def get_limit(self) -> int:
        """Get upper limit temperature of simulated DUT"""
        return self._get_device().get_limit()

    @keyword("Set Limit")
    def set_limit(self, limit: int) -> None:
        """Set upper limit temperature of simulated DUT"""
        self._get_device().set_limit(limit)

    @keyword("Reset Device")
    def reset(self) -> None:
        """Reset simulated DUT"""
        self._get_device().reset()

