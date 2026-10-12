from robot.api.deco import keyword, library
from robot.api import logger as robot_logger

from embedded_test_lab.device import Device
from embedded_test_lab.transports import SimulatorTransport, SerialTransport, RetryingTransport


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
        self.device = Device(SimulatorTransport())
        robot_logger.info("Opened simulator DUT")

    @keyword("Close Device")
    def close_device(self) -> None:
        self.device = None

    @keyword("Get Temperature")
    def get_temperature(self) -> int:
        return self._get_device().get_temperature()

    @keyword("Set Temperature")
    def set_temperature(self, temperature: int) -> None:
        self._get_device().set_temperature(temperature)

    @keyword("Get Status")
    def get_status(self) -> str:
        return self._get_device().get_status()

    @keyword("Set Status")
    def set_status(self, status: str) -> None:
        self._get_device().set_status(status)

    @keyword("Get Limit")
    def get_limit(self) -> int:
        return self._get_device().get_limit()

    @keyword("Set Limit")
    def set_limit(self, limit: int) -> None:
        self._get_device().set_limit(limit)

    @keyword("Reset Device")
    def reset(self) -> None:
        self._get_device().reset()

    @keyword("Open Serial Device")
    def open_serial_device(
            self,
            port: str = "/dev/ttyACM0",
            baudrate: int = 115200,
    ) -> None:
        transport = SerialTransport(
            port=port,
            baudrate=baudrate,
        )

        self.device = Device(transport)

        robot_logger.info(
            f"Opened serial DUT: {port} @ {baudrate}"
        )

    @keyword("Close Serial Device")
    def close_serial_device(self) -> None:
        if self.device is not None:
            transport = self.device.transport

            if hasattr(transport, "close"):
                transport.close()

            self.device = None
            robot_logger.info("DUT connection closed")

    @keyword("Open Retrying Serial Device")
    def open_retrying_serial_device(
            self,
            port: str = "/dev/ttyACM0",
            baudrate: int = 115200,
    ) -> None:
        transport = RetryingTransport(SerialTransport(
            port=port,
            baudrate=baudrate,
        ), retry_delay=0.1)

        self.device = Device(transport)

        robot_logger.info(
            f"Opened serial DUT: {port} @ {baudrate}"
        )

    @keyword("Close Retrying Serial Device")
    def close_retrying_serial_device(self) -> None:
        if self.device is not None:
            transport = self.device.transport

            if hasattr(transport, "close"):
                transport.close()

            self.device = None
            robot_logger.info("DUT connection closed")

    @keyword("FIT Set Response Delay")
    def set_fit_limit(self, command: str) -> None:
        response = self._get_device().transport.send(f"{command}")
        robot_logger.info(response)

    @keyword("Clear Input Buffer")
    def clear_input_buffer(self) -> None:
        device = self._get_device()
        transport = device.transport

        if hasattr(transport, "clear_input_buffer"):
            transport.clear_input_buffer()
