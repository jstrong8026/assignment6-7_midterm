from app.exceptions import CalculatorError, ValidationError
from app.input_validation import parse_number
from app.operations import OperationFactory

class CalculatorREPL:
    def __init__(self, calculator, max_input_value=None, input_fn=input, output_fn=print):
        self.calculator = calculator
        self.max_input_value = max_input_value
        self._input = input_fn
        self._output = output_fn
    
    def run(self):
        self._output("Welcome to Joe's REPL calculator-o-matic 5000! \n Type 'help' for instructions or type 'exit' to quit.")
        while True:
            try:
                command = self._input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                self._output("")
                break

            if command == "exit":
                break
            if not command:
                continue

            try:
                self._run_operation(command)
            except CalculatorError as error:
                self._output(f"Error: {error}")
        
        self._output("Goodbye!") 

    def _run_operation(self, command):
        OperationFactory.create(command)

        operands = self._read_operands()
        if operands is None:
            self._output("Cancelled.")
            return

        a, b = operands
        result = self.calculator.calculate(command, a, b)
        self._output(f"Result: {result}")

    def _read_operands(self):
        first = self._read_number("First number (or 'cancel'):")
        if first is None:
            return None
        second = self._read_number("Second number (or 'cancel'):")
        if second is None:
            return None
        return first, second

    def _read_number(self, prompt):
        while True:
            text = self._input(prompt).strip()
            if text.lower() == "cancel":
                return None
            try: 
                return parse_number(text, self.max_input_value)
            except ValidationError as error:
                self._output(f"Error: {error}")

