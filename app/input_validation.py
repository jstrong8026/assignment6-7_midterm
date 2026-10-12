import math
from app.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


def parse_number(text, max_input_value=None):
    try:
        value = Decimal(str(text).strip())
    except InvalidOperation:
        raise ValidationError(f"Stop playing around - '{text}' is not a valid number.") from None
    
    if not value.is_finite():
        raise ValidationError(f"Stop playing around - '{text}' is not a valid number.")

    if max_input_value is not None and abs(value) > max_input_value:
        raise ValidationError(
            f"Sorry, {text} is too large: pick something between "
            f"-{max_input_value} and {max_input_value}"
        )  
    return value

