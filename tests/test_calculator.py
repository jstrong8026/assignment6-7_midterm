import pytest
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError

def test_calculate_resturns_the_expected_result():
    assert Calculator().calculate("+", 2, 3) == 5

def test_calculate_records_a_calculation_in_history():
    calc = Calculator()
    calc.calculate("add", 2, 3)

    assert len(calc.history) == 1
    entry = calc.history[0]
    assert entry.operation == "add"
    assert (entry.operand_a, entry.operand_b, entry.result) == (2, 3, 5)

def test_failed_calculation_is_not_recorded():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.calculate("/", 1, 0)
    assert calc.history == []

def test_unknown_operation_is_not_recorded():
    calc = Calculator()
    with pytest.raises(ValidationError):
        calc.calculate("spinach", 1, 2)
    assert calc.history == []