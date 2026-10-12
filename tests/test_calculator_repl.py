from decimal import Decimal
import pytest
from app.calculator import Calculator
from app.calculator_repl import CalculatorREPL
from app.operations import OperationFactory

def make_repl(inputs, calculator=None, **kwargs):
    """Build a REPL that 'types' the given lines and records what it prints."""
    outputs = []
    feed = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError from None
    
    repl = CalculatorREPL(
        calculator or Calculator(),
        input_fn=fake_input,
        output_fn=outputs.append,
        **kwargs,
    )
    return repl, outputs

def test_exit_ends_loop():
    repl, output = make_repl(["exit"])
    repl.run()
    assert output[-1] == "Goodbye!"

def test_end_of_input_exits_gracefully():
    repl, output = make_repl([])
    repl.run()
    assert output[-1] == "Goodbye!"

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
    assert output[-1] == "Goodbye!"

@pytest.mark.parametrize("command", [
    "add", "subtract", "multiply", "divide", "power", "root",
    "modulus", "int_divide", "percent", "abs_diff",
])
def test_every_required_command_is_a_registered_name(command):
    OperationFactory.create(command)