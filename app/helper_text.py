from app.operations import ALL_OPERATIONS

COMMANDS = [
    ("history", "Shows the calculation history"),
    ("clear", "Clears the calculation history (can be undone)"),
    ("undo", "Undo the last change"),
    ("redo", "Redo the last undone change"),
    ("save", "Save the calculation history to a .CSV file"),
    ("load", "Load the history from the .CSV file"),
    ("help", "Brings up this help menu"),
    ("exit", "Quit the calculator"),
]


def get_helper_text():
    lines = [
        "",
        "HOW TO USE JOE'S REPL CALCULATOR-O-MATIC 5000",
        "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-",
        "Type a calculation command (add, subtract, etc.), then enter two numbers when prompted.",
        "Type 'cancel' at a number prompt to abandon the calculation.",
        "",
        "Numbers:",
        "- You can use a whole number (5) or a decimal (5.0)",
        "- Use a period (.) for decimals, not a comma (,)",
        "- Don't be cheeky and try to use letters instead of numbers - complex numbers like 'i' or 'pi' are not allowed.",
        "",
        "Calculation commands (these are the symbols or words you can use to perform calculations):",
    ]

    for operation_class in ALL_OPERATIONS:
        names = " or ".join(f"'{name}'" for name in operation_class.names)
        description = getattr(operation_class, "description", "")
        line = f"- {names}"
        if description: 
            line += f" - {description}"
        lines.append(line)

    lines += [
        "Capital letters and extra spaces will be ignored, so don't stress about them.",
        "",
        "Other Commands (you can enter these at any prompt):"]
    for name, description in COMMANDS:
        lines.append(f"  {name:<8} -  {description}")
    lines.append("")
    return "\n".join(lines)
