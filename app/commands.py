from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol, Tuple
from .calculator import Calculator
from .input_validators import parse_two_numbers
from .exceptions import ValidationError

class Command(Protocol):
    def execute(self, argv: List[str]) -> str: ...

@dataclass
class CalcOpCommand:
    name: str
    calculator: Calculator

    def execute(self, argv: List[str]) -> str:
        a, b = parse_two_numbers(argv, self.calculator.cfg)
        result = self.calculator.calculate(self.name, a, b)
        return f"Result: {result}"

@dataclass
class SimpleCommand:
    """Wraps zero-arg calculator helpers."""
    func: Callable[[], str | None]

    def execute(self, argv: List[str]) -> str:
        msg = self.func()
        return msg or ""

class CommandFactory:
    """Creates commands, encapsulating REPL logic from __main__."""
    def __init__(self, calculator: Calculator):
        self.calculator = calculator
        self._registry: Dict[str, Callable[[List[str]], str]] = {}
        self._install_defaults()

    def _install_defaults(self):
        # Register operation commands dynamically from calculator
        for name in self.calculator.available_operations():
            self.register(name, lambda argv, n=name: CalcOpCommand(n, self.calculator).execute(argv))

        # Utility commands
        self.register("history", lambda argv: self._cmd_history())
        self.register("clear",   lambda argv: self._cmd_clear())
        self.register("undo",    lambda argv: "Undone last operation." if self.calculator.undo() else "Nothing to undo.")
        self.register("redo",    lambda argv: "Redid last operation." if self.calculator.redo() else "Nothing to redo.")
        self.register("save",    lambda argv: f"History saved to {self.calculator.save_history()}")
        self.register("load",    lambda argv: f"Loaded {self.calculator.load_history()} history entries.")
        self.register("help",    lambda argv: self.calculator.dynamic_help())

    def register(self, name: str, handler: Callable[[List[str]], str]):
        self._registry[name] = handler

    def execute(self, name: str, argv: List[str]) -> Tuple[bool, str]:
        fn = self._registry.get(name)
        if not fn:
            return False, f"Unknown command '{name}'. Type 'help'."
        try:
            return True, fn(argv)
        except Exception as ex:
            return True, f"Error: {ex}"

    def _cmd_history(self) -> str:
        lines = []
        for i, c in enumerate(self.calculator.history_list(), 1):
            lines.append(f"{i:3d}. {c.operation}({c.a}, {c.b}) = {c.result} @ {c.timestamp}")
        return "\n".join(lines) if lines else "(no history)"

    def _cmd_clear(self) -> str:
        self.calculator.clear_history()
        return "History cleared."
