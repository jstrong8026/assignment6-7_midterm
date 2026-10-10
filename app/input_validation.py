import math

def parse_number(text):
    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"Stop playing around - '{text}' is not a valid number.")
    if not math.isfinite(value):
        raise ValueError(f"Stop playing around - '{text}' is not a valid number.")
    return value

