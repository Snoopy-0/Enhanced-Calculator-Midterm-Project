from dataclasses import dataclass
from typing import Callable, Dict
from .exceptions import OperationError

# Operation classes (Command-like objects with a common interface)
@dataclass
class Operation:
    func: Callable[[float, float], float]
    name: str
    help: str

    def execute(self, a: float, b: float) -> float:
        return self.func(a, b)

class OperationFactory:
    _registry: Dict[str, Operation] = {}

    @classmethod
    def register(cls, name: str, func: Callable[[float, float], float], help_text: str):
        cls._registry[name] = Operation(func, name, help_text)

    @classmethod
    def create(cls, name: str) -> Operation:
        op = cls._registry.get(name)
        if not op:
            raise OperationError(f"Unknown operation '{name}'")
        return op

    @classmethod
    def names(cls):
        return sorted(cls._registry.keys())

    @classmethod
    def help_map(cls):
        return {n: cls._registry[n].help for n in cls._registry}

# Concrete operation functions
def _safe_div(a: float, b: float) -> float:
    if b == 0:
        raise OperationError("Division by zero")
    return a / b

def _power(a: float, b: float) -> float:
    # negative powers allowed; guard huge exponents
    if abs(b) > 1e6:
        raise OperationError("Exponent too large")
    return a ** b

def _root(a: float, b: float) -> float:
    # nth root: b-th root of a
    if b == 0:
        raise OperationError("Zeroth root is undefined")
    if a < 0 and int(b) % 2 == 0:
        raise OperationError("Even root of negative number")
    return (a ** (1.0 / b))

def _mod(a: float, b: float) -> float:
    if b == 0:
        raise OperationError("Modulus by zero")
    return a % b

def _int_div(a: float, b: float) -> float:
    if b == 0:
        raise OperationError("Integer division by zero")
    return a // b

def _percent(a: float, b: float) -> float:
    if b == 0:
        raise OperationError("Percentage denominator cannot be zero")
    return (a / b) * 100.0

def _absdiff(a: float, b: float) -> float:
    return abs(a - b)

# Basic arithmetic
def _add(a: float, b: float) -> float: return a + b
def _sub(a: float, b: float) -> float: return a - b
def _mul(a: float, b: float) -> float: return a * b
def _div(a: float, b: float) -> float: return _safe_div(a, b)

# Register operations (Decorator-like helper)
def register_operation(name: str, help_text: str):
    def deco(fn):
        OperationFactory.register(name, fn, help_text)
        return fn
    return deco

# Use decorator to auto-register and build dynamic help
@register_operation("add", "Add two numbers: add a b")
def add(a, b): return _add(a, b)

@register_operation("subtract", "Subtract two numbers: subtract a b")
def subtract(a, b): return _sub(a, b)

@register_operation("multiply", "Multiply two numbers: multiply a b")
def multiply(a, b): return _mul(a, b)

@register_operation("divide", "Divide two numbers: divide a b")
def divide(a, b): return _div(a, b)

@register_operation("power", "Power: a^b")
def power(a, b): return _power(a, b)

@register_operation("root", "Root: b-th root of a")
def root(a, b): return _root(a, b)

@register_operation("modulus", "Modulus: a % b")
def modulus(a, b): return _mod(a, b)

@register_operation("int_divide", "Integer division: a // b")
def int_divide(a, b): return _int_div(a, b)

@register_operation("percent", "Percentage: (a / b) * 100")
def percent(a, b): return _percent(a, b)

@register_operation("abs_diff", "Absolute difference: |a - b|")
def abs_diff(a, b): return _absdiff(a, b)
