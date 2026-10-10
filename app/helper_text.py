from app.operations import ALL_OPERATIONS

def get_helper_text():
    lines = [
        "",
        "HOW TO USE JOE'S REPL CALCULATOR-O-MATIC 5000",
        "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-",
        "You'll be asked to provide a first number, a mathematical operation, and then a second number.",
        "",
        "Numbers:",
        "- You can use a whole number (5) or a decimal (5.0)",
        "- Use a period (.) for decimals, not a comma (,)",
        "- Don't be cheeky and try to use letters instead of numbers - complex numbers like 'i' or 'pi' are not allowed.",
        "",
        "Operations (these are the symbols or words you can use to perform calculations):",
    ]

    for operation_class in ALL_OPERATIONS:
        names = " or ".join(f"'{name}'" for name in operation_class.names)
        description = getattr(operation_class, "description", "")
        line = f"- {names}"
        if description: 
            line += f" - {description}"
        lines.append(line)

    lines += [
        "  (Capital letters and extra spaces will be ignored, so don't stress about them.)",
        "",
        "Commands (you can enter these at any prompt):",
        "  help - Displays the list of supported commands",
        "  exit - Exits the calculator",
        "",
        "That's it! Now Math to your heart's content!",
        "",
    ]

    return "\n".join(lines)