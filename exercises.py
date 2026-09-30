DO NOT TOUCH


class Device:
    temperature = 0
    limit = 0
    status = 'PRE_INIT'

    def __init__(self):
        self.temperature = 20
        self.limit = 80
        self.status = 'READY'

    def reset(self):
        self.temperature = 20
        self.limit = 80
        self.status = 'READY'

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
    parameter, value = response.strip().split(":")
    if len(parameter) == 0 or  len(value) == 0:
        raise ValueError
    print(f'("{parameter}", "{value}")')


if __name__ == '__main__':
    parse_response("       TEMP:25    ")
    parse_response("STATUS:READY")

    device = Device()

    device.get_temperature()

    device.set_temperature(35)

    device.get_temperature()
    device.reset()
    device.get_temperature()