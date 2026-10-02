def parse_response(response: str) -> tuple[str, str]:
    parameter, value = response.split(":")
    parameter = parameter.strip()
    value = value.strip()

    if not parameter or not value:
        raise ValueError
    return parameter, value
