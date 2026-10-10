from app.operations import get_operation
from app.input_validation import parse_number
from app.helper_text import get_helper_text

def ask(prompt):
    while True:
        text=input(prompt).strip()
        if text.lower() in ("exit", "'exit'"):
            return None
        if text.lower() in ("help", "'help'"):
            print(get_helper_text())
            continue
        return text

def main():
    print("Welcome to Joe's REPL calculator-o-matic 5000! \n Type 'help' for instructions or type 'exit' to quit.")

    while True:
        first = ask("Enter the first number: ")
        if first is None:
            break
        
        symbol = ask("Enter the mathematical operation (ie: + or Multiply): ")
        if symbol is None:
            break
        
        second = ask("Enter the second number: ")
        if second is None:
            break

        try:
            a = parse_number(first)
            b = parse_number(second)
            operation = get_operation(symbol)
            print("Result:", operation.calculate(a, b))
        except ValueError as error:
            print("Error:", error)
   

        print() #this is just a line break to make the output look nicer

    print("Thanks for using Joe's REPL calculator-o-matic 5000! Goodbye!")

if __name__ == "__main__":
    main()
