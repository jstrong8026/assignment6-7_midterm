import pytest
from app.exceptions import ValidationError
from app.operations import ALL_OPERATIONS, Addition, OperationFactory

def test_create_returns_the_right_operation():
    assert isinstance(OperationFactory.create("+"), Addition)

def test_create_ignores_case_and_spaces():
    assert isinstance(OperationFactory.create(" ADD "), Addition)

def test_create_unknown_name_raises_validation_error():
    with pytest.raises(ValidationError, match="spinach"):
        OperationFactory.create("spinach")

@pytest.mark.parametrize("operation_class", ALL_OPERATIONS)
def test_every_name_creates_its_operation(operation_class):
    for name in operation_class.names:
        assert isinstance(OperationFactory.create(name), operation_class)

