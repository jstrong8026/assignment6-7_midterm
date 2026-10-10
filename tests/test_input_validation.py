import pytest
from app.input_validation import parse_number
from app.exceptions import ValidationError

@pytest.mark.parametrize("text, expected", [
    ("5", 5.0),
    ("-2.5", -2.5),
    (" 7 ", 7.0),
])
def test_parse_number_valid(text, expected):
    assert parse_number(text) == expected

@pytest.mark.parametrize("text", ["Z", "abc", "", "1,5", "nan", "inf"])
def test_parse_number_invalid(text):
    with pytest.raises(ValidationError, match="Stop playing around - '.*' is not a valid number."):
        parse_number(text)
