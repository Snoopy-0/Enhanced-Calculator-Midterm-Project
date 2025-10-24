from typing import Sequence, Tuple
from .exceptions import ValidationError
from .calculator_config import Config

def parse_two_numbers(args: Sequence[str], cfg: Config) -> Tuple[float, float]:
    if len(args) != 2:
        raise ValidationError("Expected two numbers, e.g., 'add 2 3'")
    try:
        a = float(args[0])
        b = float(args[1])
    except ValueError:
        raise ValidationError("Inputs must be numeric")
    for val in (a, b):
        if abs(val) > cfg.MAX_INPUT_VALUE:
            raise ValidationError(f"Input {val} exceeds maximum allowed value {cfg.MAX_INPUT_VALUE}")
    return a, b
