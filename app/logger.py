import logging
from pathlib import Path
from app.exceptions import ConfigurationError

class Logger:
    """Writes log messages to a file using standard logging module"""

    def __init__(self, log_file: str | Path, encoding: str = "utf-8"):
        try:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file, encoding=encoding)
        except OSError as error:
            raise ConfigurationError(
                f"Cannot open log file '{log_file}': {error.strerror or 'unknown error'}"
            ) from None
        
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self._handler = handler
        self._logger = logging.getLogger("calculator")
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(self._handler)
        

    def info(self, message, *args):
        self._logger.info(message, *args)

    def warning(self, message, *args):
        self._logger.warning(message, *args)

    def error(self, message, *args, exc_info=False):
        self._logger.error(message, *args, exc_info=exc_info)

    def close(self):
        self._logger.removeHandler(self._handler)
        self._handler.close()



