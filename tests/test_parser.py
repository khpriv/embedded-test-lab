import pytest
from embedded_test_lab.protocol import parse_response


def test_parser_response():
    assert parse_response("TEST:25") == ('TEST', '25')
    assert parse_response("    TEST:25     ") == ('TEST', '25')
    assert parse_response("STATUS:NOT_READY") == ('STATUS', 'NOT_READY')

    with pytest.raises(ValueError):
        parse_response("A:B:C")
    with pytest.raises(ValueError):
        parse_response("TEST:")
    with pytest.raises(ValueError):
        parse_response(":25")
    with pytest.raises(ValueError):
        parse_response("garbage")


@pytest.mark.parametrize(
    "response, expected",
    [
        ("TEST:25", ("TEST", "25")),
        ("   TEST:25   ", ("TEST", "25")),
        ("TEST : 25", ("TEST", "25")),
    ],
    ids=[
        "normal",
        "outer-whitespace",
        "field-whitespace",
    ],
)
def test_valid_response(response, expected):
    assert parse_response(response) == expected


@pytest.mark.parametrize(
    "response",
    [
        ":",
        "TEST:",
        ":25",
        "garbage",
        "A:B:C",
    ],
)
def test_invalid_response(response):
    with pytest.raises(ValueError):
        parse_response(response)
