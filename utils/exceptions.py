"""
Custom exception classes for SymCalc.
"""
class SymCalcError(Exception):
    """Base exception for SymCalc errors."""
    pass

class ParseError(SymCalcError):
    """Error in expression parsing."""
    pass

class ValidationError(SymCalcError):
    """Error in input validation."""
    pass

class EnvironmentError(SymCalcError):
    """Error in environment management."""
    pass

class CommandError(SymCalcError):
    """Error in command execution."""
    pass

class ConversionError(SymCalcError):
    """Error in unit conversion."""
    pass
