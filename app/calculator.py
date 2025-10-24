from typing import List, Protocol
import math
from .calculator_config import Config
from .exceptions import OperationError, ValidationError
from .operations import OperationFactory
from .calculation import Calculation
from .history import History

class Observer(Protocol):
    def update(self, calc: Calculation) -> None: ...

class LoggingObserver:
    def __init__(self, logger):
        self.logger = logger
    def update(self, calc: Calculation) -> None:
        self.logger.info(f"{calc.operation}({calc.a}, {calc.b}) = {calc.result} @ {calc.timestamp}")

class AutoSaveObserver:
    def __init__(self, cfg: Config, history: History):
        self.cfg = cfg
        self.history = history
    def update(self, calc: Calculation) -> None:
        if self.cfg.AUTO_SAVE:
            # Use pandas to save
            self.history.save_csv(self.cfg.HISTORY_FILE, self.cfg.DEFAULT_ENCODING)

class Calculator:
    def __init__(self, cfg: Config, logger):
        self.cfg = cfg
        self.logger = logger
        self.history = History(cfg.MAX_HISTORY_SIZE)
        self.observers: List[Observer] = [LoggingObserver(logger), AutoSaveObserver(cfg, self.history)]

    # Decorator-powered dynamic help, sourced from OperationFactory registry
    def dynamic_help(self) -> str:
        lines = ["Available commands:"]
        lines.extend([f"  {name:12s} - {help_text}" for name, help_text in OperationFactory.help_map().items()])
        lines += [
            "  history      - Show history",
            "  clear        - Clear history",
            "  undo         - Undo last change",
            "  redo         - Redo last undo",
            "  save         - Save history to CSV",
            "  load         - Load history from CSV",
            "  help         - Show this help",
            "  exit         - Quit"
        ]
        return "\n".join(lines)

    def available_operations(self) -> List[str]:
        return OperationFactory.names()

    def _round(self, value: float) -> float:
        return round(value, self.cfg.PRECISION)

    def calculate(self, operation_name: str, a: float, b: float) -> float:
        # validate ranges
        for val in (a, b):
            if abs(val) > self.cfg.MAX_INPUT_VALUE:
                raise ValidationError(f"Input {val} exceeds maximum allowed value {self.cfg.MAX_INPUT_VALUE}")
        op = OperationFactory.create(operation_name)
        result = op.execute(a, b)
        if math.isfinite(result) is False:
            raise OperationError("Non-finite result")
        result = self._round(result)
        c = Calculation.create(operation_name, a, b, result)
        self.history.add(c)
        self._notify(c)
        return result

    def _notify(self, calc: Calculation):
        for obs in self.observers:
            try:
                obs.update(calc)
            except Exception:
                # Observers shouldn't break core flow
                self.logger.error("Observer failed", exc_info=True)

    # History-facing helpers
    def history_list(self):
        return self.history.list()

    def clear_history(self):
        self.history.clear()

    def undo(self) -> bool:
        return self.history.undo()

    def redo(self) -> bool:
        return self.history.redo()

    def save_history(self) -> str:
        return self.history.save_csv(self.cfg.HISTORY_FILE, self.cfg.DEFAULT_ENCODING)

    def load_history(self) -> int:
        return self.history.load_csv(self.cfg.HISTORY_FILE, self.cfg.DEFAULT_ENCODING)
