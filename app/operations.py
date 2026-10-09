from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict



#the user input name and class are together so it's easier to add new entries later
class Addition:
    names = ("+", "add")
    def calculate(self, a, b):
        return a + b

class Subtraction:
    names = ("-", "subtract")
    def calculate(self, a, b):
        return a - b

class Multiplication: 
    names = ("*", "multiply", "times")
    def calculate(self, a, b):
        return a * b

class Division:
    names = ("/", "divide", "divided by", "over")
    def calculate(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero - you just broke the internet!")
        return a / b

class Power: 
    names = ("^", "power")
    def calculate(self, a, b):
        return a ** b

class Root: 
    names = ("root",)  
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


ALL_OPERATIONS = [Addition, Subtraction, Multiplication, Division, Power, Root]


OPERATIONS = {}
for operation_class in ALL_OPERATIONS:
    for name in operation_class.names:
        OPERATIONS[name] = operation_class   

def get_operation(user_input):
    key = user_input.strip().lower() #this lets the user input be case insensitive
    if key not in OPERATIONS:
        raise ValueError(f"The mathematical operation '{user_input}' is not supported - type 'help' for a list of supported operations.")
    
    return OPERATIONS[key]()
