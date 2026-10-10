import pytest
from app.exceptions import (
    CalculatorError, ValidationError, OperationError, ConfigurationError,
)

@pytest.mark.parametrize("error_class", [
    ValidationError, OperationError, ConfigurationError,
])

def test_errors_are_calculator_errors(error_class):
    with pytest.raises(CalculatorError):
        raise error_class("something went wrong")

def test_message_is_kept():
    with pytest.raises(OperationError, match="bad operation"):
        raise OperationError("bad operation")



