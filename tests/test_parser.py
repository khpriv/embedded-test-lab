import pytest
from exercises import parse_response


def test_parser_response():
    assert parse_response("TEST:25") == ('TEST', '25')
    assert parse_response("    TEST:25     ") == ('TEST', '25')

    with pytest.raises(ValueError):
        parse_response(" : ")

    with pytest.raises(ValueError):
        parse_response("TEST:")
    with pytest.raises(ValueError):
        parse_response(":25")
    with pytest.raises(ValueError):
        parse_response("garbage")
