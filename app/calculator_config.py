import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

def _get_int(values, name, default):
    raw = values.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ConfigurationError(f"{name} must be a whole number, but got '{raw}'") from None

def _get_float(values, name, default):
    raw = values.get(name)
    if raw is None:
        return default
    try: 
        return float(raw)
    except ValueError:
        raise ConfigurationError(f"{name} must be a number, but got '{raw}'") from None

def _get_bool(values, name, default): 
    raw = values.get(name)
    if raw is None:
        return default
    text = raw.strip().lower()
    if text == "true":
        return True
    if text == "false":
        return False
    raise ConfigurationError(f"{name} must be 'true' or 'false', but got '{raw}'")


@dataclass(frozen=True)
class CalculatorConfig:
    log_dir: Path = Path("logs")
    history_dir: Path = Path("history")
    log_file: str = "calculator.log"
    history_file: str = "calculator_history.csv"
    max_history_size: int = 100
    auto_save: bool = True
    precision: int = 2
    max_input_value: float = 1_000_000
    default_encoding: str = "utf-8"

    @property
    def log_path(self) -> Path:
        return self.log_dir / self.log_file

    @property
    def history_path(self) -> Path:
        return self.history_dir / self.history_file

    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls.from_mapping(os.environ)

    @classmethod
    def from_mapping(cls, values):
        config = cls(
            log_dir=Path(values.get("CALCULATOR_LOG_DIR", "logs")),
            history_dir=Path(values.get("CALCULATOR_HISTORY_DIR", "history")),
            log_file=values.get("CALCULATOR_LOG_FILE", "calculator.log"),
            history_file=values.get("CALCULATOR_HISTORY_FILE", "calculator_history.csv"),
            max_history_size=_get_int(values, "CALCULATOR_MAX_HISTORY_SIZE", 100), 
            auto_save=_get_bool(values, "CALCULATOR_AUTO_SAVE", True),
            precision=_get_int(values, "CALCULATOR_PRECISION", 2),
            max_input_value=_get_float(values, "CALCULATOR_MAX_INPUT_VALUE", 1_000_000),
            default_encoding=values.get("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
        )
        config.validate()
        return config

    def validate(self):
        if self.max_history_size <1:
            raise ConfigurationError("CALCULATOR_MAX_HISTORY_SIZE must be at least 1")
        if self.precision <0:
            raise ConfigurationError("CALCULATOR_PRECISION cannot be negative - how would that even work?")
        if self.max_input_value <= 0:
            raise ConfigurationError("CALCULATOR_MAX_INPUT_VALUE must be greater than 0 - not much point in having a calculator if you're just adding 0 and 0")
        try:
            "".encode(self.default_encoding)
        except LookupError:
            raise ConfigurationError(
                f"CALCULATOR_DEFAULT_ENCODING '{self.default_encoding}' is not a known encoding. Please use utf-8") from None
        
    
