from typing import Protocol
from transports import SimulatorTransport


class Transport(Protocol):
    def send(self, command: str) -> str:
        pass

class Device:
    def __init__(self, transport: Transport) -> None:
        self.transport = transport

    def reset(self) -> None:
        response = self.transport.send("RESET")

        if response != "OK":
            raise RuntimeError(f"Reset failed: {response}")

    def get_temperature(self) -> int:
        try:
            parameter, value = parse_response(self.transport.send("GET_TEMP"))
        except ValueError:
            raise RuntimeError(f"Incorrect response")

        if parameter == "TEMP":
            return int(value)
        else:
            raise RuntimeError(f"Expected TEMP response, got {parameter}:{value} instead")

    def set_temperature(self, new_temperature: int) -> None:
        response = self.transport.send(f"SET_TEMP:{new_temperature}")
        if response == "OK":
            return
        elif response == "ERR:OUT_OF_RANGE":
            raise ValueError(f"Failed to set temperature. {new_temperature} is out of range.")
        else:
            raise RuntimeError(f"Failed to set temperature: {response}")

    def get_status(self) -> str:
        try:
            parameter, value = parse_response(self.transport.send("GET_STATUS"))
        except ValueError:
            raise RuntimeError(f"Incorrect response")

        if parameter == "STATUS":
            return value
        else:
            raise RuntimeError(f"Expected STATUS response, got {parameter}:{value} instead")

    def set_status(self, new_status: str) -> None:
        response = self.transport.send(f"SET_STATUS:{new_status}")

        if response != "OK":
            raise RuntimeError(f"Failed to set status: {response}")

    def get_limit(self) -> int:
        try:
            parameter, value = parse_response(self.transport.send("GET_LIMIT"))
        except ValueError:
            raise RuntimeError(f"Incorrect response")

        if parameter == "LIMIT":
            return int(value)
        else:
            raise RuntimeError(f"Expected LIMIT response, got {parameter}:{value} instead")

    def set_limit(self, new_limit: int) -> None:
        response = self.transport.send(f"SET_LIMIT:{new_limit}")

        if response != "OK":
            raise RuntimeError(f"Failed to set limit: {response}")


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