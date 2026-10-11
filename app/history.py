from abc import ABC, abstractmethod
from app.calculation import Calculation

class HistoryObserver(ABC):
    """this class is for anything that needs to be told when a calculation is recorded"""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """called by the Calculator after each successful calculation"""

