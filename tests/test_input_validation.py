import pytest
from app.input_validation import parse_number
from app.exceptions import ValidationError
from decimal import Decimal

@pytest.mark.parametrize("text, expected", [
    ("5", Decimal("5.0")),
    ("-2.5", Decimal("-2.5")),
    (" 7 ", Decimal("7.0")),
    ("0.1", Decimal("0.1")),
])
def test_parse_number_valid(text, expected):
    assert parse_number(text) == expected

def test_parse_number_returns_decimal():
    assert isinstance(parse_number("5"), Decimal)


@pytest.mark.parametrize("text", ["Z", "abc", "", "1,5", "nan", "-inf"])
def test_parse_number_invalid(text):
    with pytest.raises(ValidationError, match="Stop playing around - '.*' is not a valid number."):
        parse_number(text)

@pytest.mark.parametrize("text", ["1001", "-1001"])
def test_value_beyond_limit_is_rejected(text):
    with pytest.raises(ValidationError, match="too large"):
        parse_number(text, max_input_value=Decimal("1000"))

def test_value_matching_limit_is_allowed():
    assert parse_number("1000", max_input_value=Decimal("1000")) == Decimal("1000")

def test_no_limit_by_default():
    assert parse_number("99999999999999999999") == Decimal ("99999999999999999999")
    