from dataclasses import dataclass

@dataclass(frozen=True)
class CalculatorMemento:
    """makes the calculator history snapshot read-only"""
    history: tuple 