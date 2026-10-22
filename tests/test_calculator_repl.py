from decimal import Decimal
import pytest
from app.calculator import Calculator
from app.calculator_repl import CalculatorREPL
from app.operations import OperationFactory
from app.helper_text import get_helper_text
from tests.fakes import FakeLogger
from colorama import Fore, Style
from app.colors import Colorizer

def make_repl(inputs, calculator=None, logger=None, **kwargs):
    """Build a REPL that 'types' the given lines and records what it prints."""
    outputs = []
    feed = iter(inputs)

    def fake_input(prompt=""):
        try:
            value = next(feed)
        except StopIteration:
            raise EOFError from None
        if isinstance(value, BaseException):
            raise value 
        return value 
    
    repl = CalculatorREPL(
        calculator or Calculator(),
        logger or FakeLogger(),
        input_fn=fake_input,
        output_fn=outputs.append,
        **kwargs,
    )
    return repl, outputs

def test_exit_ends_loop():
    repl, output = make_repl(["exit"])
    repl.run()
    assert output[-1] == "Goodbye - thank you for doing math with me!"

def test_end_of_input_exits_gracefully():
    repl, output = make_repl([])
    repl.run()
    assert output[-1] == "Goodbye - thank you for doing math with me!"

def test_operation_command_prints_results():
    repl, output = make_repl(["add", "2", "3", "exit"])
    repl.run()
    assert "Result: 5" in output

def test_calculation_is_recorded_in_history():
    calc = Calculator()
    repl, _ = make_repl(["add", "2", "3", "exit"], calc)
    repl.run()
    assert len(calc.history) == 1

def test_commands_ignore_case_and_spaces():
    repl, output = make_repl(["  ADD  ", "2", "3", "exit"])
    repl.run()
    assert "Result: 5" in output

def test_blank_line_is_ignored():
    repl, output = make_repl(["", "add", "1", "1", "exit"])
    repl.run()
    assert "Result: 2" in output

def test_unknown_command_reports_error_and_continues():
    repl, output = make_repl(["spinach", "add", "1", "1", "exit"])
    repl.run()
    assert any("not supported" in line for line in output)
    assert "Result: 2" in output

def test_invalid_number_is_asked_again():
    repl, output = make_repl(["add", "abc", "2", "3", "exit"])
    repl.run()
    assert any("not a valid number" in line for line in output)
    assert "Result: 5" in output

def test_number_above_limit_is_asked_again():
    repl, output = make_repl(
        ["add", "5000", "2", "3", "exit"], max_input_value=Decimal("1000"))
    repl.run()
    assert any("too large" in line for line in output)
    assert "Result: 5" in output

@pytest.mark.parametrize("inputs", [
    ["add", "cancel", "exit"],
    ["add", "2", "cancel", "exit"],
])
def test_cancel_abandons_calculation(inputs):
    calc = Calculator()
    repl, output = make_repl(inputs, calc)
    repl.run()
    assert "Cancelled." in output
    assert calc.history == []

def test_calculation_errors_reported_not_raised():
    repl, output = make_repl(["divide", "1", "0", "exit"])
    repl.run()
    assert any("zero" in line for line in output)
    assert output[-1] == "Goodbye - thank you for doing math with me!"

@pytest.mark.parametrize("command", [
    "add", "subtract", "multiply", "divide", "power", "root",
    "modulus", "int_divide", "percent", "abs_diff",
])
def test_every_required_command_is_a_registered_name(command):
    OperationFactory.create(command)

def test_history_lists_calcualations():
    repl, output = make_repl(["add", "2", "3", "history", "exit"])
    repl.run()
    assert any(line.startswith("1.") and "= 5" in line for line in output)

def test_history_when_empty():
    repl, output = make_repl(["history", "exit"])
    repl.run()
    assert "No calculations yet - make some math!" in output

def test_clear_empties_history():
    calc = Calculator()
    repl, output = make_repl(["add", "2", "3", "clear", "exit"], calc)
    repl.run()
    assert calc.history == []
    assert "History cleared - you are now a blank slate." in output

def test_clear_on_empty_history_notification():
    repl, output = make_repl(["clear", "exit"])
    repl.run()
    assert "History is already empty." in output

def test_undo_and_redo():
    calc = Calculator()
    repl, output = make_repl(["add", "2", "3", "undo", "redo", "exit"], calc)
    repl.run()
    assert "Undid last change." in output
    assert "Redid last change." in output
    assert len(calc.history) == 1

@pytest.mark.parametrize("command, message", [
    ("undo", "Nothing to undo"),
    ("redo", "Nothing to redo"),
])
def test_undo_redo_with_nothing_to_do_report_error(command, message):
    repl, output = make_repl([command, "exit"])
    repl.run()
    assert any(message in line for line in output)
    assert output[-1] == "Goodbye - thank you for doing math with me!"


def test_save_then_load_roundtrip(tmp_path):
    calc = Calculator()
    repl, _= make_repl(
        ["add", "2", "3", "save", "clear", "load", "exit"],
        calc,
        history_path=tmp_path / "history.csv",
    )
    repl.run()
    assert [entry.result for entry in calc.history] == [5]

def test_save_and_load_without_configured_path_error():
    repl, output = make_repl(["save", "load", "exit"])
    repl.run()
    assert sum("No history file" in line for line in output) == 2

def test_load_missing_file_reports_error(tmp_path):
    repl, output = make_repl(["load", "exit"], history_path=tmp_path / "nope.csv")
    repl.run()
    assert any("not found" in line for line in output)

def test_help_command_shows_help_text():
    repl, output = make_repl(["help", "exit"])
    repl.run()
    assert get_helper_text() in output

def test_help_mentions_every_repl_command():
    repl, _= make_repl([])
    text = get_helper_text().lower()
    for name in list(repl._commands) + ["exit"]:
        assert name in text

#adding new tests for logs
class BrokenCalculator(Calculator):
    def calculate(self, operation_name, a, b):
        raise RuntimeError("boom")


def _messages(repl, level):
    return [message for lvl, message in repl.logger.records if lvl == level]


def test_start_stop_and_commands_are_logged_at_info():
    repl, _ = make_repl(["history", "exit"])
    repl.run()
    info = _messages(repl, "INFO")
    assert "Calculator started" in info
    assert "Command: history" in info
    assert "Calculator stopped" in info


def test_failed_commands_are_logged_as_warnings():
    repl, _ = make_repl(["undo", "exit"])
    repl.run()
    assert any("Nothing to undo" in message for message in _messages(repl, "WARNING"))


def test_unexpected_errors_are_logged_as_errors_and_the_loop_continues():
    repl, output = make_repl(["add", "1", "1", "exit"], BrokenCalculator())
    repl.run()
    assert any("Unexpected error" in line for line in output)
    assert any("add" in message for message in _messages(repl, "ERROR"))
    assert output[-1] == "Goodbye - thank you for doing math with me!"


def test_interrupt_in_the_middle_of_a_calculation_exits_cleanly():
    calc = Calculator()
    repl, output = make_repl(["add", KeyboardInterrupt()], calc)
    repl.run()
    assert output[-1] == "Goodbye - thank you for doing math with me!"
    assert calc.history == []


def test_end_of_input_in_the_middle_of_a_calculation_exits_cleanly():
    repl, output = make_repl(["add", "2"])
    repl.run()
    assert output[-1] == "Goodbye - thank you for doing math with me!"

def test_save_failure_is_reported_not_raised(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("I am a file, not a folder")
    repl, output = make_repl(["save", "exit"], history_path=blocker / "history.csv")

    repl.run()

    assert any("could not be written" in line for line in output)
    assert output[-1] == "Goodbye - thank you for doing math with me!"


#testing colorizer add-on
def test_colored_output_wraps_results_and_errors():
    repl, output = make_repl(
        ["add", "2", "3", "undo", "undo", "exit"], colors=Colorizer(enabled=True)
    )
    repl.run()

    assert Fore.GREEN + "Result: 5" + Style.RESET_ALL in output
    assert any(
        line.startswith(Fore.RED) and "Nothing to undo" in line for line in output
    )