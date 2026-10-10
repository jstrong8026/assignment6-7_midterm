#Generic calculator errors
class CalculatorError(Exception): 
    pass

#invalid user input
class ValidationError(CalculatorError): 
    pass

#operation can't be performed
class OperationError(CalculatorError): 
    pass

#configuration settings are no good
class ConfigurationError(CalculatorError):
    pass