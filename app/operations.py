from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict



#the user input name and class are together so it's easier to add new entries later
class Addition:
    names = ("+", "add")
    description = "Adds the first number to the second number."
    def calculate(self, a, b):
        return a + b

class Subtraction:
    names = ("-", "subtract")
    description = "Subtracts the second number from the first number."
    def calculate(self, a, b):
        return a - b

class Multiplication: 
    names = ("*", "multiply", "times")
    description = "Multiplies the first number by the second number."
    def calculate(self, a, b):
        return a * b

class Division:
    names = ("/", "divide", "divided by", "over")
    description = "Divides the first number by the second number."
    def calculate(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero - you just broke the internet!")
        return a / b

class IntegerDivision:
    names = ("//", "integer divide", "floor divide")
    description = "Divides the first number by the second number and then rounds down to a whole number (ie: leaves off the remainder)."
    def calculate(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero - you just broke the internet!")
        return a // b
    
class Power: 
    names = ("^", "power")
    description = "Raises the first number to the power of the second number."
    def calculate(self, a, b):
        return a ** b

class Root: 
    names = ("root",)
    description = "Takes the root of the first number to the degree of the second number."
    def calculate(self, a, b): 
        if b == 0: 
            raise ValueError("Root degree cannot be zero - you just broke the internet!")
        if a < 0: 
            if b != int(b) or int(b) %2 == 0:
                raise ValueError(
                    "Cannot take the root of a negative number - your math teacher would be disappointed in you."
                )
            return -((-a) ** (1 / b))
        return a ** (1 / b)


ALL_OPERATIONS = [Addition, Subtraction, Multiplication, Division, Power, Root, IntegerDivision]


OPERATIONS = {}
for operation_class in ALL_OPERATIONS:
    for name in operation_class.names:
        OPERATIONS[name] = operation_class   

def get_operation(user_input):
    key = user_input.strip().lower() #this lets the user input be case insensitive
    if key not in OPERATIONS:
        raise ValueError(f"The mathematical operation '{user_input}' is not supported - type 'help' for a list of supported operations.")
    
    return OPERATIONS[key]()
