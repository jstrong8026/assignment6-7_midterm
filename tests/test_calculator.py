import pytest
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError, ConfigurationError

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

def test_clear_history_empties_history():
    calc = Calculator()
    calc.calculate("add", 2, 3)

    calc.clear_history()

    assert calc.history == []

def test_undo_restores_cleared_history():
    calc = Calculator()
    calc.calculate("add", 2, 3)
    calc.clear_history()

    calc.undo()

    assert len(calc.history) == 1

def test_clearing_empty_history_crates_no_undo_step():
    calc = Calculator()
    calc.clear_history()

    with pytest.raises(OperationError, match="Nothing to undo - you can't undo what was never done!"):
        calc.undo()

def test_history_is_capped_at_max_size():
    calc = Calculator(max_history_size=2)
    calc.calculate("add", 1, 1)
    calc.calculate("add", 2, 2)
    calc.calculate("add", 3, 3)

    assert [entry.result for entry in calc.history] == [4, 6]

def test_no_limit_by_default():
    calc = Calculator()
    for number in range(150):
        calc.calculate("add", number, 1)

    assert len(calc.history) == 150

def test_undo_restores_dropped_entry():
    calc = Calculator(max_history_size=2)
    calc.calculate("add", 1, 1)
    calc.calculate("add", 2, 2)
    calc.calculate("add", 3, 3)

    calc.undo()

    assert [entry.result for entry in calc.history] == [2, 4]

@pytest.mark.parametrize("bad_size", [0, -1])
def test_invalid_max_history_size_rejected(bad_size):
    with pytest.raises(ConfigurationError):
        Calculator(max_history_size=bad_size)





