from colorama import Fore, Style

class Colorizer: 
    """Wraps text in color codes, or can be switched off"""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def _paint(self, text, color):
        if not self.enabled:
            return text
        return f"{color}{text}{Style.RESET_ALL}"

    def success(self, text):
        return self._paint(text, Fore.GREEN)

    def error(self, text):
        return self._paint(text, Fore.RED)

    def info(self, text):
        return self._paint(text, Fore.CYAN)
    