class CalculatorError(Exception):
    """Base class for calculator errors."""

class OperationError(CalculatorError):
    """Raised when an operation fails (e.g., invalid input, divide by zero)."""

class ValidationError(CalculatorError):
    """Raised when input validation fails."""
