import pytest
from dataclasses import FrozenInstanceError
from app.calculation import Calculation
from app.exceptions import ValidationError
from decimal import Decimal

def test_to_dict_has_expected_keys():
    data = Calculation("Add", Decimal(2), Decimal(3), Decimal(5)).to_dict()
    assert set(data) == {"operation", "operand_a", "operand_b", "result", "timestamp"}

def test_round_trip_gives_back_equal_calculation():
    original = Calculation("Add", Decimal(2), Decimal(3), Decimal(5))
    restored = Calculation.from_dict(original.to_dict())
    assert restored == original

def test_calculation_cannot_be_modified():
    calc = Calculation("Add", Decimal(2), Decimal(3), Decimal(5))
    with pytest.raises(FrozenInstanceError):
        calc.result = 99 # type: ignore
        #intentionally ignoring this as the test is ensuring it won't get any restult

def test_from_dict_with_missing_field_raises():
    data = Calculation("add", Decimal(2), Decimal(3), Decimal(5)).to_dict()
    del data["result"]

    with pytest.raises(ValidationError, match="Missing field"):
        Calculation.from_dict(data)        