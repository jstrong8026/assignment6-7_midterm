import logging

from app.calculator_config import CalculatorConfig
from app.logger import setup_logging

def test_setup_logging_writes_to_path_from_config(tmp_path):
    config = CalculatorConfig(log_dir=tmp_path / "logs", log_file="test.log")

    handler = setup_logging(config.log_path, config.default_encoding)
    try: 
        logging.getLogger("calculator").info("hello log")
        handler.flush()
    finally:
        logging.getLogger("calculator").removeHandler(handler)
        handler.close()

    assert config.log_path.exists()
    assert "hello log" in config.log_path.read_text(encoding="utf-8")