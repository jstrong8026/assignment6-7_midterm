from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ConfigurationError
from app.operations import OperationFactory
from decimal import ROUND_HALF_UP, Decimal, DecimalException, Overflow
from app.history import load_history, save_history
from pathlib import Path

class Calculator:
    def __init__(self, max_history_size: int | None = None, precision: int | None = None):
        if max_history_size is not None and max_history_size < 1:
            raise ConfigurationError("max_history_size must be at least 1")
        if precision is not None and precision < 0:
            raise ConfigurationError("precision cannot be negative")
        self.max_history_size = max_history_size
        self.precision = precision
        self.history = []
        self._undo_stack = []
        self._redo_stack = []
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def _notify(self, calculation):
        for observer in self._observers:
            observer.update(calculation)

    #this looks for changes in history
    def _notify_history_changed(self):
        for observer in self._observers:
            observer.history_changed()

    def _snapshot(self):
        return CalculatorMemento(tuple(self.history))

    def calculate(self, operation_name, a, b):
        operation = OperationFactory.create(operation_name)
        a, b = Decimal(str(a)), Decimal(str(b))
        try:
            raw_result = operation.calculate(a, b)
        except Overflow:
            raise OperationError("That result is way too large to show - try a calculation with a smaller answer.") from None
        except DecimalException:
            raise OperationError("Halt! This operation cannot be performed with those values") from None

        if not raw_result.is_finite():
            raise OperationError("Result is not a finite number - I don't go to infinity nor beyond")
        if raw_result == 0:
            raw_result = Decimal(0)
        result = self._apply_precision(raw_result)
        calculation = Calculation(operation.names[0], a, b, result)
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history.append(calculation)
        self._trim_history()
        self._notify(calculation)
        return result

    def undo(self):
        if not self._undo_stack:
            raise OperationError("Nothing to undo - you can't undo what was never done!")
        self._redo_stack.append(self._snapshot())
        self.history = list(self._undo_stack.pop().history)
        self._notify_history_changed()

    def redo(self):
        if not self._redo_stack:
            raise OperationError("Nothing to redo - make some calculations, undo them, then try to redo")
        self._undo_stack.append(self._snapshot())
        self.history = list(self._redo_stack.pop().history)
        self._notify_history_changed()

    def clear_history(self):
        if not self.history:
            return
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history = []
        self._notify_history_changed()

    #this is a helper to enforce max history
    def _trim_history(self):
        if self.max_history_size is None:
            return
        while len(self.history) > self.max_history_size:
            self.history.pop(0)

    def _apply_precision(self, value):
        if self.precision is None:
            return value
        if value.as_tuple().exponent >= -self.precision:
            return value
        step = Decimal(10) ** -self.precision
        return value.quantize(step, rounding=ROUND_HALF_UP)

    def save(self, file_path: str | Path, encoding: str = "utf-8"):
        save_history(self.history, file_path, encoding)

    def load(self, file_path: str | Path, encoding: str = "utf-8"):
        loaded = load_history(file_path, encoding)
        if loaded == self.history:
            return
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history = loaded
        self._trim_history()
        self._notify_history_changed()