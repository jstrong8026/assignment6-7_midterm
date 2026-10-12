import pytest
import logging
import pandas as pd
from app.calculator import Calculator
from app.history import HistoryObserver, LoggingObserver, AutoSaveObserver, save_history
from app.exceptions import OperationError


class RecordingObserver(HistoryObserver):
    def __init__(self):
        self.received = []

    def update(self, calculation):
        self.received.append(calculation)

#this is for my code that allows updates during a clear, undo, etc.
class ChangeCountingObserver(HistoryObserver):
    def __init__(self):
        self.changes = 0

    def update(self, calculation):
        pass

    def history_changed(self):
        self.changes += 1

#testing basic observer functions
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

#makes sure you can't directly create a history observer
def test_history_observer_cannot_be_created_directly():
    with pytest.raises(TypeError):
        HistoryObserver() # pyright: ignore[reportAbstractUsage]
        #ignoring this warning as it's expected

#checking observer is logging messages
def test_logging_observer_logs_each_calculation(caplog):
    calc = Calculator()
    calc.register_observer(LoggingObserver())

    with caplog.at_level(logging.INFO,logger="calculator"):
        calc.calculate("add", 2, 3)

    assert len(caplog.records) == 1
    message = caplog.records[0].getMessage()
    assert "add" in message
    assert "5" in message

def test_logging_observer_ignores_failed_calculations(caplog):
    calc = Calculator()
    calc.register_observer(LoggingObserver())

    with caplog.at_level(logging.INFO, logger="calculator"):
        with pytest.raises(Exception):
            calc.calculate("/", 1, 0)

    assert caplog.records == []

#creating tests for pandas to create csv file
def test_auto_save_writes_csv_after_calculation(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.register_observer(AutoSaveObserver(calc, csv_file))

    calc.calculate("add", 2, 3)

    df = pd.read_csv(csv_file)
    assert len(df) == 1
    assert df.loc[0, "operation"] == "add"
    assert df.loc[0, "result"] == 5

def test_autosave_saves_full_history(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.register_observer(AutoSaveObserver(calc, csv_file))

    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 4, 5)

    assert len(pd.read_csv(csv_file)) == 2

def test_autosave_creates_missing_folder(tmp_path):
    csv_file = tmp_path / "nested" / "history.csv"
    calc = Calculator()
    calc.register_observer(AutoSaveObserver(calc, csv_file))

    calc.calculate("add", 2, 3)

    assert csv_file.exists()

def test_failed_calculation_does_not_save(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.register_observer(AutoSaveObserver(calc, csv_file))

    with pytest.raises(Exception):
        calc.calculate("/", 1, 0)

    assert not csv_file.exists()

def test_save_with_empty_history_keeps_headers(tmp_path):
    csv_file = tmp_path / "history.csv"

    save_history([], csv_file)

    df = pd.read_csv(csv_file)
    assert len(df) == 0
    assert list(df.columns) == ["operation", "operand_a", "operand_b", "result", "timestamp"]


def test_undo_redo_clear_announce_history_changes():
    calc = Calculator()
    observer = ChangeCountingObserver()
    calc.register_observer (observer)

    calc.calculate("add", 1, 1)
    assert observer.changes == 0

    calc.undo()
    assert observer.changes == 1
    calc.redo()
    assert observer.changes == 2
    calc.clear_history()
    assert observer.changes == 3


def test_failed_undo_does_not_announce_change():
    calc = Calculator()
    observer = ChangeCountingObserver()
    calc.register_observer(observer)

    with pytest.raises(OperationError):
        calc.undo()

    assert observer.changes == 0

def test_autosave_file_follows_undo_redo_clear(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.register_observer(AutoSaveObserver(calc, csv_file))
    calc.calculate("add", 2, 3)
    calc.calculate("multiply", 4, 5)

    calc.undo()
    assert len(pd.read_csv(csv_file)) == 1

    calc.redo()
    assert len(pd.read_csv(csv_file)) == 2

    calc.clear_history()
    assert len(pd.read_csv(csv_file)) == 0

    calc.undo()
    assert len(pd.read_csv(csv_file)) == 2