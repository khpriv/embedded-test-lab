
class Device:
    def __init__(self):
        self.temperature = 20
        self.limit = 80
        self.status = 'READY'

    def reset(self):
        self.__init__()

    def get_temperature(self) -> int:
        return self.temperature

    def set_temperature(self, new_temperature: int):
        if new_temperature > self.limit:
            raise ValueError
        else:
            self.temperature = new_temperature

    def get_status(self) -> str:
        return self.status

    def set_status(self, new_status: str):
        self.status = new_status

    def get_limit(self):
        return self.limit

    def set_limit(self, new_limit: int):
        self.limit = new_limit


def parse_response (response: str):
    parameter, value = response.replace(" ", "").split(":")
    if len(parameter) == 0 or  len(value) == 0:
        raise ValueError
    return parameter, value


if __name__ == '__main__':
    print(parse_response("       TEMP:  25    "))
    print(parse_response("STATUS:READY"))
    device = Device()

    device.get_temperature()

    device.set_temperature(35)

    device.get_temperature()
    device.reset()
    device.get_temperature()