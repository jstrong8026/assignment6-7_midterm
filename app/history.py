import pandas as pd
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from app.calculation import Calculation

class HistoryObserver(ABC):
    """this class is for anything that needs to be told when a calculation is recorded"""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """called by the Calculator after each successful calculation"""

class LoggingObserver(HistoryObserver):
    """writes a log line for every calculatin"""

    def update(self, calculation: Calculation) -> None:
        logging.getLogger("calculator").info(
            "Calculation: %s %s %s = %s",
            calculation.operand_a,
            calculation.operation, 
            calculation.operand_b,
            calculation.result,   
        )

class AutoSaveObserver(HistoryObserver):
    """Saves the full history to a csv file after each calculation"""

    def __init__(self, calculator, file_path="history/calculator_history.csv"):
        self.calculator = calculator
        self.file_path = file_path

    def update(self, calculation: Calculation) -> None:
        save_history(self.calculator.history, self.file_path)

#adding the pandas save history option
COLUMNS = ["operation", "operand_a", "operand_b", "result", "timestamp"]

def save_history(history, file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    rows = [calculation.to_dict() for calculation in history]
    pd.DataFrame(rows, columns=COLUMNS) .to_csv(file_path, index=False)