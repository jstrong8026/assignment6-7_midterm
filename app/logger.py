import logging
from pathlib import Path

#creating the actual logging file
def setup_logging(log_file="logs/calculator.log"):
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    return handler