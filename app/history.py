from abc import ABC, abstractmethod
from app.calculation import Calculation
import logging

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
