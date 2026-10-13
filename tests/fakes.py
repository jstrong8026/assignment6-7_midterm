class FakeLogger:
    """stands in for app.logger.Logger and records what was logged."""

    def __init__(self):
        self.records = []

    def _record(self, level, message, args):
        self.records.append((level, message % args if args else message))

    def info(self, message, *args):
        self._record("INFO", message, args)

    def warning(self, message, *args):
        self._record("WARNING", message, args)

    def error(self, message, *args, exc_info=False):
        self._record("ERROR", message, args)