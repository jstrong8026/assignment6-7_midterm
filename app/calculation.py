from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from app.exceptions import ValidationError

def _to_decimal(value):
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        raise ValidationError(f"'{value}' is not a valid number") from None
    if not number.is_finite():
        raise ValidationError(f"'{value}' is not a valid number")
    return number
    
@dataclass(frozen=True)
class Calculation:
    operation: str
    operand_a: Decimal
    operand_b: Decimal
    result: Decimal
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
        try:
            return cls(
                operation=str(data["operation"]),
                operand_a=_to_decimal(data["operand_a"]),
                operand_b=_to_decimal(data["operand_b"]),
                result=_to_decimal(data["result"]),
                timestamp=datetime.fromisoformat(data["timestamp"]), 
        )
        except KeyError as error:
            raise ValidationError(f"Missing field {error}") from None
        except (TypeError, ValueError):
            raise ValidationError("Invalid timestamp") from None
        