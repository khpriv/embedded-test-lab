from typing import Protocol
from transports import SimulatorTransport


class DeviceProtocolError(RuntimeError):
    pass


class Transport(Protocol):
    def send(self, command: str) -> str:
        ...


class Device:
    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def reset(self) -> None:
        self._expect_ok("RESET")


    def get_temperature(self) -> int:
        value = self._get_value("GET_TEMP", "TEMP")

        try:
            return int(value)
        except ValueError as exc:
            raise DeviceProtocolError(
                f"Invalid TEMP value: {value!r}"
            ) from exc


    def set_temperature(self, new_temperature: int) -> None:
        response = self.transport.send(f"SET_TEMP:{new_temperature}")

        if response == "OK":
            return

        if response == "ERR:OUT_OF_RANGE":
            raise ValueError(f"Failed to set temperature. {new_temperature} is out of range.")
        
        raise RuntimeError(f"Failed to set temperature: {response}")


    def get_status(self) -> str:
        value = self._get_value("GET_STATUS", "STATUS")
        return value


    def set_status(self, new_status: str) -> None:
        self._expect_ok(f"SET_STATUS:{new_status}")


    def get_limit(self) -> int:
        value = self._get_value("GET_LIMIT", "LIMIT")

        try:
            return int(value)
        except ValueError as exc:
            raise DeviceProtocolError(
                f"Invalid LIMIT value: {value!r}"
            ) from exc


    def set_limit(self, new_limit: int) -> None:
        self._expect_ok(f"SET_LIMIT:{new_limit}")


    def _get_value(self, command: str, expected_parameter: str) -> str:
        response = self.transport.send(f"{command}")

        try:
            parameter, value = parse_response(response)
        except ValueError as exc:
            raise DeviceProtocolError(
                f"Malformed response to {command}: {response!r}"
            ) from exc

        if parameter != f"{expected_parameter}":
            raise DeviceProtocolError(
                f"Expected {command} response, got {response!r}"
            )
        return value


    def _expect_ok(self, command: str) -> None:
        response = self.transport.send(f"{command}")
        if response != "OK":
            raise RuntimeError(f"Failed to {command}: {response}")


def parse_response (response: str) -> tuple[str, str]:
    parameter, value = response.split(":")
    parameter = parameter.strip()
    value = value.strip()

    if not parameter or not value:
        raise ValueError
    return parameter, value


if __name__ == '__main__':
    print(parse_response("       TEMP:  25    "))
    print(parse_response("STATUS:READY"))

    transport = SimulatorTransport()
    device = Device(transport)
    print(device.get_temperature())
    print(device.set_temperature(35))
    print(device.get_temperature())
    print(device.reset())
    print(device.get_temperature())