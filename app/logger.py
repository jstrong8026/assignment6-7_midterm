import logging
from pathlib import Path

#creating the actual logging file
#adding note for utf-8 encoding
def setup_logging(log_file: str | Path = "logs/calculator.log", encoding: str = "utf-8"):
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_file, encoding=encoding)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    return handler


