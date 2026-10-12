import pytest
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError
from decimal import Decimal

def test_defaults_when_nothing_is_set():
    config = CalculatorConfig.from_mapping({})

    assert config.log_path == Path("logs") / "calculator.log"
    assert config.history_path == Path("history") / "calculator_history.csv"
    assert config.max_history_size == 100
    assert config.auto_save is True

def test_values_are_read_and_converted():
    config = CalculatorConfig.from_mapping({
        "CALCULATOR_LOG_DIR": "my_logs",
        "CALCULATOR_LOG_FILE": "app.log", 
        "CALCULATOR_MAX_HISTORY_SIZE": "25",
        "CALCULATOR_AUTO_SAVE": "FALSE",
        "CALCULATOR_PRECISION": "9",
        "CALCULATOR_MAX_INPUT_VALUE": "500",
    })

    assert config.log_path == Path("my_logs") / "app.log"
    assert config.max_history_size == 25
    assert config.auto_save is False
    assert config.precision == 9
    assert config.max_input_value == Decimal("500")

@pytest.mark.parametrize("name, value", [
    ("CALCULATOR_MAX_HISTORY_SIZE", "lots"),
    ("CALCULATOR_MAX_HISTORY_SIZE", "0"), 
    ("CALCULATOR_PRECISION", "-1"),
    ("CALCULATOR_MAX_INPUT_VALUE", "abc"),
    ("CALCULATOR_MAX_INPUT_VALUE", "0"),
    ("CALCULATOR_MAX_INPUT_VALUE", "nan"),
    ("CALCULATOR_AUTO_SAVE", "maybe"), 
    ("CALCULATOR_DEFAULT_ENCODING", ".mp4"),

])

def test_invalid_settings_raise_configuration_error(name, value):
    with pytest.raises(ConfigurationError, match=name):
        CalculatorConfig.from_mapping({name: value})

def test_from_env_reads_env_variables(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "1")

    assert CalculatorConfig.from_env().precision == 1