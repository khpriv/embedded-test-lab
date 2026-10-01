class SimulatorTransport:
    DEFAULT_TEMPERATURE = 20
    DEFAULT_LIMIT = 80
    DEFAULT_STATUS = 'READY'

    def __init__(self) -> None:
        self.temperature = self.DEFAULT_TEMPERATURE
        self.limit = self.DEFAULT_LIMIT
        self.status = self.DEFAULT_STATUS

    def send(self, command: str) -> str:
        command = command.strip()
        if ":" in command:
            try:
                parameter, value = command.split(":")
            except ValueError:
                return "ERR:INVALID_COMMAND"
            parameter = parameter.strip()
            value = value.strip()

            match parameter:
                case "SET_TEMP":
                    return self._set_temperature(value)
                case "SET_LIMIT":
                    return self._set_limit(value)
                case "SET_STATUS":
                    return self._set_status(value)
                case _:
                    return "ERR:UNKNOWN_COMMAND"
        else:
            match command:
                case "GET_TEMP":
                    return self._get_temperature()
                case "GET_LIMIT":
                    return self._get_limit()
                case "GET_STATUS":
                    return self._get_status()
                case "RESET":
                    return self._reset()
                case _:
                    return "ERR:UNKNOWN_COMMAND"

    def _reset(self) -> str:
        self.temperature = self.DEFAULT_TEMPERATURE
        self.limit = self.DEFAULT_LIMIT
        self.status = self.DEFAULT_STATUS
        return "OK"

    def _get_temperature(self) -> str:
        return f"TEMP:{self.temperature}"

    def _set_temperature(self, new_temperature: str) -> str:
        try:
            new_temperature = int(new_temperature)
        except ValueError:
            return "ERR:INVALID_VALUE"
        if new_temperature > self.limit:
            return "ERR:OUT_OF_RANGE"
        else:
            self.temperature = new_temperature
            return "OK"

    def _get_status(self) -> str:
        return f"STATUS:{self.status}"

    def _set_status(self, new_status: str) -> str:
        self.status = new_status
        return "OK"

    def _get_limit(self) -> str:
        return f"LIMIT:{self.limit}"

    def _set_limit(self, new_limit: str) -> str:
        try:
            self.limit = int(new_limit)
        except ValueError:
            return "ERR:INVALID_VALUE"
        return "OK"


class FakeTransport:
    def __init__(self, response: str) -> None:
        self.response = response
        self.last_command = None

    def send(self, command: str) -> str:
        self.last_command = command
        return self.response


