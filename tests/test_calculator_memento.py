import pytest
from dataclasses import FrozenInstanceError
from app.calculator import Calculator
from app.calculator_memento import CalculatorMemento

def test_memento_cannot_be_modified():
    memento = CalculatorMemento(())
    with pytest.raises(FrozenInstanceError):
        memento.history = ("changed",)

def test_snapshot_is_not_affected_by_later_calculations():
    calc = Calculator()
    calc.calculate("add", 1, 1)
    snapshot = calc._snapshot()

    calc.calculate("add", 2, 2)

    assert len(snapshot.history) == 1