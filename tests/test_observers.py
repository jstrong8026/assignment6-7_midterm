import pytest
from app.calculator import Calculator
from app.history import HistoryObserver
from app.exceptions import OperationError

class RecordingObserver(HistoryObserver):
    def __init__(self):
        self.received = []

    def update(self, calculation):
        self.received.append(calculation)

def test_observer_is_notified_of_calculation():
    calc = Calculator()
    observer = RecordingObserver()
    calc.register_observer(observer)

    calc.calculate("add", 2, 3)

    assert len(observer.received) == 1
    assert observer.received[0].result == 5

def test_every_registered_observer_is_notified():
    calc = Calculator()
    first, second = RecordingObserver(), RecordingObserver()
    calc.register_observer(first)
    calc.register_observer(second)

    calc.calculate("add", 2, 3)

    assert len(first.received) == 1
    assert len(second.received) == 1

def test_removed_observer_is_not_notified():
    calc = Calculator()
    observer = RecordingObserver()
    calc.register_observer(observer)
    calc.remove_observer(observer)

    calc.calculate("add", 2, 3)

    assert observer.received == []

def test_failed_calculation_does_not_notify_observers():
    calc = Calculator()
    observer = RecordingObserver()
    calc.register_observer(observer)

    with pytest.raises(OperationError):
        calc.calculate("/", 1, 0)

    assert observer.received == []

def test_history_observer_cannot_be_created_directly():
    with pytest.raises(TypeError):
        HistoryObserver() # pyright: ignore[reportAbstractUsage]
        #ignoring this warning as it's expected

