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

def test_undo_removes_last_calculation():
    calc = Calculator()
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 4, 5)

    calc.undo()

    assert len(calc.history) == 1
    assert calc.history[0].result == 5

def test_redo_restores_undone_calculation():
    calc = Calculator()
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 4, 5)

    calc.undo()
    calc.redo()

    assert len(calc.history) == 2
    assert calc.history[1].result == 20

def test_new_calculation_clears_redo():
    calc = Calculator()
    calc.calculate("add", 2, 3)
    calc.undo()
    calc.calculate("add", 1, 1)

    with pytest.raises(OperationError, match="Nothing to redo - make some calculations, undo them, then try to redo"):
        calc.redo()

def test_nothing_to_undo():
    with pytest.raises(OperationError, match="Nothing to undo - you can't undo what was never done!"):
        Calculator().undo()

def test_failed_calculation_creates_no_undo_step():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.calculate("/", 1, 0)
    with pytest.raises(OperationError, match="Nothing to undo - you can't undo what was never done!"):
        calc.undo()

