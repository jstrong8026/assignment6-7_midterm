from app.operations import get_operation

def main():
    print("Welcome to Joe's REPL calculator-o-matic 5000! \n Type exit to quit, or help for a list of supported operations.")

    while True:
        first = input("Enter the first number: ")
        if first.lower() == "exit":
            break
        
        symbol = input("Enter the mathematical operation (ie: + or Multiply): ")
        if symbol.lower() == "exit":
            break
        
        second = input("Enter the second number: ")
        if second.lower() == "exit":
            break

        try:
            a = float(first)
            b = float(second)
        except ValueError:
            print("Error:  Please enter valid numbers.")
            continue

        try:
            operation = get_operation(symbol)
            print("Result: ", operation.calculate(a, b))
        except ValueError as error:
            print("Error:", error)

        print() #this is just a line break to make the output look nicer

    print("Thanks for using Joe's REPL calculator-o-matic 5000! Goodbye!")

if __name__ == "__main__":
    main()
