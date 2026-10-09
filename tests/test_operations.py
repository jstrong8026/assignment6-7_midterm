import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.operations import get_operation

#I am allowing users to enter a symbol or word for the calculation
@pytest.mark.parametrize("symbol, a, b, expected", [
    ("+", 2, 3, 5),
    ("add", 2, 3, 5),
    ("-", 5, 2, 3),
    ("subtract", 5, 2, 3),
    ("*", 4, 3, 12),
    ("multiply", 4, 3, 12),
    ("times", 4, 3, 12),
    ("/", 10, 2, 5),
    ("divide", 10, 2, 5),
    ("divided by", 10, 2, 5),
    ("over", 10, 2, 5),
    ("^", 2, 3, 8),
    ("power", 2, 3, 8),
    ("root", 27, 3, 3)

])

def test_operations(symbol, a, b, expected):
    result = get_operation(symbol).calculate(a, b)
    assert result == pytest.approx(expected)

def test_divide_by_zero():
    with pytest.raises(ValueError):
        get_operation("/").calculate(5, 0)

def test_odd_root_of_negative():
    assert get_operation("root").calculate(-8, 3) == pytest.approx(-2)

def test_even_root_of_negative():
    with pytest.raises(ValueError):
        get_operation("root").calculate(-4, 2)

def test_unknown_symbol():
    with pytest.raises(ValueError):
        get_operation("%")
