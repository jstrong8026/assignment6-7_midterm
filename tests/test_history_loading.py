from decimal import Decimal
import pytest
from app.calculator import Calculator
from app.exceptions import OperationError
from app.history import load_history, save_history

HEADER = "operation,operand_a,operand_b,result,timestamp\n"

def test_save_then_load_gives_equal_history(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.calculate("add", Decimal("0.1"), Decimal("0.2"))
    calc.calculate("/", 1, 3)

    save_history(calc.history, csv_file)

    assert load_history(csv_file) == calc.history


def test_loading_keeps_decimal_values(tmp_path):
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    calc.calculate("add", Decimal("0.1"), Decimal("0.2"))
    save_history(calc.history, csv_file)

    loaded = load_history(csv_file)

    assert loaded[0].result == Decimal("0.3")
    assert isinstance(loaded[0].result, Decimal)


def test_header_only_file_loads_empty(tmp_path):
    csv_file = tmp_path / "history.csv"
    save_history([], csv_file)

    assert load_history(csv_file) == []


def test_missing_file_raises(tmp_path):
    with pytest.raises(OperationError, match="not found"):
        load_history(tmp_path / "nope.csv")


def test_completely_empty_file_raises(tmp_path):
    csv_file = tmp_path / "history.csv"
    csv_file.write_text("")

    with pytest.raises(OperationError, match="could not be read"):
        load_history(csv_file)


def test_missing_columns_raises(tmp_path):
    csv_file = tmp_path / "history.csv"
    csv_file.write_text("operation,result\nadd,5\n")

    with pytest.raises(OperationError, match="missing columns"):
        load_history(csv_file)


@pytest.mark.parametrize("row", [
    "add,abc,3,5,2026-10-12T13:07:00",
    "add,2,3,5,not-a-time",
    "spinach,2,3,5,2026-10-12T13:07:00",
    "add,2,3,,2026-10-12T13:07:00",
    "add,2,3,nan,2026-10-12T13:07:00"
])
def test_bad_rows_report_their_row_number(tmp_path, row):
    csv_file = tmp_path / "history.csv"
    csv_file.write_text(HEADER + row + "\n")

    with pytest.raises(OperationError, match="row 2"):
        load_history(csv_file)