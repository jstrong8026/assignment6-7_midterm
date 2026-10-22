from app.operations import ALL_OPERATIONS
from app.helper_text import get_helper_text

def test_help_lists_every_operation_name():
    text = get_helper_text().lower()
    for operation_class in ALL_OPERATIONS:
        for name in operation_class.names:
            assert name in text, f"'{name}' is missing from the help text"

def test_help_mentions_commands():
    text = get_helper_text().lower()
    assert "help" in text
    assert "exit" in text

def test_help_explains_disabling_color_option():
    assert "NO_COLOR" in get_helper_text()