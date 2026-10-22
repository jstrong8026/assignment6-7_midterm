from app.exceptions import CalculatorError, OperationError, ValidationError
from app.helper_text import get_helper_text
from app.input_validation import parse_number
from app.operations import OperationFactory
from app.colors import Colorizer

class CalculatorREPL:
    def __init__(self, calculator, logger, max_input_value=None, history_path=None, encoding="utf-8", input_fn=input, output_fn=print, colors=None):
        self.calculator = calculator
        self.logger = logger
        self.max_input_value = max_input_value
        self.history_path = history_path
        self.encoding = encoding
        self._input = input_fn
        self._output = output_fn
        self.colors = colors or Colorizer(enabled=False)
        self._commands = {
            "history": self._show_history,
            "clear": self._clear_history,
            "undo": self._undo,
            "redo": self._redo,
            "save": self._save,
            "load": self._load,
            "help": self._show_help,
        }
    
    def run(self):
        self.logger.info("Calculator started")
        self._show_info("Welcome to Joe's REPL calculator-o-matic 5000! \n Type 'help' for instructions or type 'exit' to quit.")
        try:
            self._loop()
        except (EOFError, KeyboardInterrupt):
            self._show_info("")
        self.logger.info("Calculator stopped")
        self._show_info("Goodbye - thank you for doing math with me!")

    def _loop(self):
        while True:
            command = self._input("Enter calculation command>").strip().lower()
            if command == "exit":
                return
            if not command:
                continue

            self.logger.info("Command: %s", command)
            try:
                self._handle(command)
            except CalculatorError as error:
                self.logger.warning("Command '%s' failed: %s", command, error)
                self._show_error(f"Error: {error}")
            except (EOFError, KeyboardInterrupt):
                raise
            except Exception:
                self.logger.error("Unexpected error in command '%s'", command, exc_info=True)
                self._show_error("Unexpected error. Details were written to the log.")
          
    
    def _handle(self, command):
        handler = self._commands.get(command)
        if handler is None:
            self._run_operation(command)
        else:
            handler()

    def _show_history(self):
        if not self.calculator.history:
            self._show_info("No calculations yet - make some math!")
            return
        for number, entry in enumerate(self.calculator.history, start=1):
            self._show_result(
                f"{number}. {entry.operation}({entry.operand_a}, {entry.operand_b})"
                f" = {entry.result}"
            )

    def _clear_history(self):
        if not self.calculator.history:
            self._show_info("History is already empty.")
            return
        self.calculator.clear_history()
        self._show_info("History cleared - you are now a blank slate.")

    def _undo(self):
        self.calculator.undo()
        self._show_info("Undid last change.")

    def _redo(self):
        self.calculator.redo()
        self._show_info("Redid last change.")

    def _save(self):
        path = self._history_file()
        self.calculator.save(path, self.encoding)
        self._show_result(f"History saved to {path}")

    def _load(self):
        path = self._history_file()
        self.calculator.load(path, self.encoding)
        self._show_result(f"History loaded from {path} ({len(self.calculator.history)} entries)")

    def _show_help(self):
        self._show_info(get_helper_text())

    def _history_file(self):
        if self.history_path is None:
            raise OperationError("No history file is configured.")
        return self.history_path            

    def _run_operation(self, command):
        OperationFactory.create(command)

        operands = self._read_operands()
        if operands is None:
            self._show_info("Cancelled.")
            return

        a, b = operands
        result = self.calculator.calculate(command, a, b)
        self._show_result(f"Result: {result}")

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
                self._show_error(f"Error: {error}")

    def _show_info(self, text):
        self._output(self.colors.info(text))

    def _show_error(self, text):
        self._output(self.colors.error(text))

    def _show_result(self, text):
        self._output(self.colors.success(text))
