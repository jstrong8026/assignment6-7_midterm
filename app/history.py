import pandas as pd
from pathlib import Path
from abc import ABC, abstractmethod
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.operations import OperationFactory

class HistoryObserver(ABC):
    """this class is for anything that needs to be told when a calculation is recorded"""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """called by the Calculator after each successful calculation"""

    #I'm adding this because the way I wrote the above code
    #the history and csv get out of synch after a clear but before the next successful calculation
    def history_changed(self) -> None:
        """Called only after undo, redo or clear"""

class LoggingObserver(HistoryObserver):
    """writes a log line for every calculatin"""

    def __init__(self, logger):
        self.logger = logger
    
    def update(self, calculation: Calculation) -> None:
        self.logger.info(
            "Calculation: %s %s %s = %s",
            calculation.operand_a,
            calculation.operation, 
            calculation.operand_b,
            calculation.result,   
        )

class AutoSaveObserver(HistoryObserver):
    """Saves the full history to a csv file after each calculation"""

    def __init__(self, calculator, file_path: str | Path = "history/calculator_history.csv", encoding: str = "utf-8", logger=None):
        self.calculator = calculator
        self.file_path = file_path
        self.encoding = encoding
        self.logger = logger

    def _save(self):
        try:
            save_history(self.calculator.history, self.file_path, self.encoding)
        except OperationError as error:
            if self.logger is None:
                raise
            self.logger.error("Auto-save failed: %s", error)

    def update(self, calculation: Calculation) -> None:
        self._save()

    #this looks for changes in history to deal wtih clear, undo, etc.
    def history_changed(self) -> None:
        self._save()

#adding the pandas save history option
COLUMNS = ["operation", "operand_a", "operand_b", "result", "timestamp"]

def save_history(history, file_path, encoding="utf-8"):
    path = Path(file_path)
    rows = [calculation.to_dict() for calculation in history]
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows, columns=COLUMNS) .to_csv(file_path, index=False, encoding=encoding)
    except OSError as error:
        raise OperationError(
            f"History file could not be written: {path} ({error.strerror or 'unknown error'})"
        ) from None

def load_history(file_path, encoding="utf-8"):
    path = Path(file_path)
    if not path.exists():
        raise OperationError(f"History file not found: {path}")

    try:
        table = pd.read_csv(path, dtype=str, keep_default_na=False, encoding=encoding)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError):
            raise OperationError(f"History file could not be read: {path}") from None

    missing = [column for column in COLUMNS if column not in table.columns]
    if missing:
        raise OperationError(f"History file is missing columns: {', '.join(missing)}")

    history = []
    for row_number, row in enumerate(table.to_dict("records"), start=2):
        try:
            OperationFactory.create(row["operation"])
            history.append(Calculation.from_dict(row))
        except ValidationError as error:
            raise OperationError(f"History file row {row_number} is invalid: {error}") from None
    return history    