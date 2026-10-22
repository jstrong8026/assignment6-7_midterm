import pytest
from colorama import Fore, Style
from app.colors import Colorizer

@pytest.mark.parametrize("method", ["success", "error", "info"])
def test_disabled_colorizer_returns_text_unchanged(method):
    assert getattr(Colorizer(enabled=False), method)("hello") == "hello"


@pytest.mark.parametrize("method, color", [
    ("success", Fore.GREEN),
    ("error", Fore.RED),
    ("info", Fore.CYAN),
])
def test_enabled_colorizer_wraps_text_in_color(method, color):
    painted = getattr(Colorizer(enabled=True), method)("hello")
    assert painted == f"{color}hello{Style.RESET_ALL}"
    