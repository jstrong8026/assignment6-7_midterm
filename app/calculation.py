from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class Calculation:
    operation: str
    operand_a: float
    operand_b: float
    result: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "operation": self.operation,
            "operand_a": self.operand_a, 
            "operand_b": self.operand_b,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            operation=data["operation"],
            operand_a=data["operand_a"],
            operand_b=data["operand_b"],
            result=data["result"],
            timestamp=datetime.fromisoformat(data["timestamp"]),    
        )