from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import OperationError, ValidationError


#the user input 'name' and 'description' are together so it's easier to add new entries later
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
            raise OperationError("Cannot divide by zero - you just broke the internet!")
        return a / b

class IntegerDivision:
    names = ("//", "integer divide", "int_divide", "floor divide")
    description = "Divides the first number by the second number and then \n rounds down to a whole number (ie: leaves off the remainder)."
    def calculate(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero - you just broke the internet!")
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
            raise OperationError("Root degree cannot be zero - you just broke the internet!")
        if a < 0: 
            if b != int(b) or int(b) %2 == 0:
                raise OperationError(
                    "Cannot take the root of a negative number - your math teacher would be disappointed in you."
                )
            return -((-a) ** (1 / b))
        return a ** (1 / b)

class Modulus:
    names = ("modulus", "mod")
    description = "Divides the first number by the second number but only returns the remainder."
    def calculate(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero - you just broke the internet!")
        return a % b

class Percent:
    names = ("percent", "percent of")
    description = "Shows A (First Number) percent of B (Second Number)."
    def calculate(self, a, b):
        if b == 0:
            raise OperationError("Cannot take the percentage of zero - you just broke a percent of the internet!")
        return (a / b) * 100

class AbsoluteDifference:
    names = ("absolute difference", "abs_diff")
    description = "Shows the distance between two numbers (always returns a positive value)"
    def calculate(self, a, b):
        return abs(a - b)

    
ALL_OPERATIONS = [Addition, Subtraction, Multiplication, Division, Power, Root, Modulus, IntegerDivision, Percent, AbsoluteDifference]


OPERATIONS = {}
for operation_class in ALL_OPERATIONS:
    for name in operation_class.names:
        OPERATIONS[name] = operation_class   

def get_operation(user_input):
    key = user_input.strip().strip("'\'").lower() #this lets the user input be case insensitive
    if key not in OPERATIONS:
        raise ValidationError(f"The mathematical operation '{user_input}' is not supported - type 'help' for a list of supported operations.")
    return OPERATIONS[key]()
