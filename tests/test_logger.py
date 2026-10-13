import logging

import pytest

from app.calculator_config import CalculatorConfig
from app.logger import Logger


@pytest.fixture
def logger(tmp_path):
    log = Logger(tmp_path / "logs" / "test.log")
    yield log
    log.close()


def test_all_three_levels_are_written(logger, tmp_path):
    logger.info("hello %s", "info")
    logger.warning("careful")
    logger.error("broken")

    text = (tmp_path / "logs" / "test.log").read_text(encoding="utf-8")
    assert "INFO - hello info" in text
    assert "WARNING - careful" in text
    assert "ERROR - broken" in text


def test_log_folder_is_created(logger, tmp_path):
    assert (tmp_path / "logs").is_dir()


def test_error_can_include_the_traceback(logger, tmp_path):
    try:
        raise ValueError("boom")
    except ValueError:
        logger.error("Something failed", exc_info=True)

    text = (tmp_path / "logs" / "test.log").read_text(encoding="utf-8")
    assert "Traceback" in text
    assert "boom" in text


def test_close_detaches_the_handler(tmp_path):
    underlying = logging.getLogger("calculator")
    before = len(underlying.handlers)
    log = Logger(tmp_path / "x.log")
    assert len(underlying.handlers) == before + 1

    log.close()

    assert len(underlying.handlers) == before


def test_logger_writes_to_the_path_from_config(tmp_path):
    config = CalculatorConfig(log_dir=tmp_path / "logs", log_file="test.log")
    log = Logger(config.log_path, config.default_encoding)
    try:
        log.info("hello log")
    finally:
        log.close()

    assert "hello log" in config.log_path.read_text(encoding="utf-8")
    