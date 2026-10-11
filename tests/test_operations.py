import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.operations import OperationFactory, Operation
from app import operations
from app.exceptions import OperationError
from app.exceptions import ValidationError


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
    ("root", 27, 3, 3),
    ("modulus", 10, 3, 1),
    ("mod", 10, 3, 1),
    ("percent", 40, 200, 20),
    ("percent of", 40, 200, 20),
    ("//", 10, 3, 3),
    ("integer divide", 10, 3, 3),
    ("int_divide", 10, 3, 3),
    ("absolute difference", 3, 10, 7),
    ("abs_diff", 3, 10, 7),

])

def test_operations(symbol, a, b, expected):
    result = OperationFactory.create(symbol).calculate(a, b)
    assert result == pytest.approx(expected)

def test_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("/").calculate(5, 0)

def test_integer_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("//").calculate(5, 0)

def test_odd_root_of_negative():
    assert OperationFactory.create("root").calculate(-8, 3) == pytest.approx(-2)

def test_even_root_of_negative():
    with pytest.raises(OperationError):
        OperationFactory.create("root").calculate(-4, 2)

def test_modulus_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("mod").calculate(5, 0)

def test_percent_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create("percent").calculate(40, 0)        

def test_unknown_symbol():
    with pytest.raises(ValidationError):
        OperationFactory.create("%")

def test_unknown_operation_message():
    with pytest.raises(ValidationError, match="spinach"):
        OperationFactory.create("spinach")

#I keep forgetting to add new operations, so I'm adding a test to make sure I add them
def test_every_operation_is_registered(): 
    for name, value in vars(operations).items():
        if isinstance(value, type) and hasattr(value, "names") and value is not operations.Operation:
            assert value in operations.ALL_OPERATIONS, f"{name} is not registered in ALL_OPERATIONS"

def test_operation_cannot_be_created_directly():
    with pytest.raises(TypeError):
        Operation()

def test_subclass_must_define_calculate():
    class Incomplete(Operation):
        pass
    with pytest.raises(TypeError):
        Incomplete()