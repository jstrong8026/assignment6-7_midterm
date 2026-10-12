from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.calculator_repl import CalculatorREPL
from app.exceptions import ConfigurationError
from app.history import AutoSaveObserver, LoggingObserver
from app.logger import setup_logging


def main():
    try:
        config = CalculatorConfig.from_env()
    except ConfigurationError as error:
        print(f"Configuration error: {error}")
        return

    setup_logging(config.log_path, config.default_encoding)

    calculator = Calculator(
        max_history_size=config.max_history_size,
        precision=config.precision,
    )
    calculator.register_observer(LoggingObserver())
    if config.auto_save:
        calculator.register_observer(
            AutoSaveObserver(calculator, config.history_path, config.default_encoding)
        )

    CalculatorREPL(calculator, max_input_value=config.max_input_value).run()

if __name__ == "__main__":
    main()
