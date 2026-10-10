import math
from app.exceptions import ValidationError

def parse_number(text):
    try:
        value = float(text)
    except ValueError:
        raise ValidationError(f"Stop playing around - '{text}' is not a valid number.") from None
    if not math.isfinite(value):
        raise ValidationError(f"Stop playing around - '{text}' is not a valid number.")
    return value

