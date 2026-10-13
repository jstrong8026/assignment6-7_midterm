from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.calculator_repl import CalculatorREPL
from app.exceptions import ConfigurationError
from app.history import AutoSaveObserver, LoggingObserver
from app.logger import Logger


def main():
    try:
        config = CalculatorConfig.from_env()
    except ConfigurationError as error:
        print(f"Configuration error: {error}")
        return

    logger = Logger(config.log_path, config.default_encoding)

    calculator = Calculator(
        max_history_size=config.max_history_size,
        precision=config.precision,
    )
    calculator.register_observer(LoggingObserver(logger))
    if config.auto_save:
        calculator.register_observer(
            AutoSaveObserver(calculator, config.history_path, config.default_encoding)
        )
    try:
        CalculatorREPL(
            calculator, 
            logger,
            max_input_value=config.max_input_value,
            history_path=config.history_path,
            encoding=config.default_encoding,
        ).run()

    finally:
        logger.close()

if __name__ == "__main__":
    main()
