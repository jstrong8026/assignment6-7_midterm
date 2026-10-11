from app.calculation import Calculation
from app.operations import OperationFactory

class Calculator:
    def __init__(self):
        self.history = []

    def calculate(self, operation_name, a, b):
        operation = OperationFactory.create(operation_name)
        result = operation.calculate(a, b)
        calculation = Calculation(operation.names[0], a, b, result)
        self.history.append(calculation)
        return result

