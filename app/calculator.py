from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError
from app.operations import OperationFactory

class Calculator:
    def __init__(self):
        self.history = []
        self._undo_stack = []
        self._redo_stack = []

    def _snapshot(self):
        return CalculatorMemento(tuple(self.history))

    def calculate(self, operation_name, a, b):
        operation = OperationFactory.create(operation_name)
        result = operation.calculate(a, b)
        calculation = Calculation(operation.names[0], a, b, result)
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history.append(calculation)
        return result

    def undo(self):
        if not self._undo_stack:
            raise OperationError("Nothing to undo - you can't undo what was never done!")
        self._redo_stack.append(self._snapshot())
        self.history = list(self._undo_stack.pop().history)

    def redo(self):
        if not self._redo_stack:
            raise OperationError("Nothing to redo - make some calculations, undo them, then try to redo")
        self._undo_stack.append(self._snapshot())
        self.history = list(self._redo_stack.pop().history)
