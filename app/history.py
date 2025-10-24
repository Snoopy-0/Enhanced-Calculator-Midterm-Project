from typing import List
import pandas as pd
from .calculation import Calculation
from .calculator_memento import Memento, Caretaker
from .exceptions import ValidationError

class History:
    def __init__(self, max_size: int):
        self._entries: List[Calculation] = []
        self._max = max_size
        self._caretaker = Caretaker()

    def snapshot(self):
        self._caretaker.push(Memento(self._entries))

    def add(self, c: Calculation):
        if len(self._entries) >= self._max:
            self._entries.pop(0)
        self.snapshot()
        self._entries.append(c)

    def list(self) -> List[Calculation]:
        return list(self._entries)

    def clear(self):
        self.snapshot()
        self._entries.clear()

    def undo(self) -> bool:
        state = self._caretaker.undo(self._entries)
        if state is None:
            return False
        self._entries = state
        return True

    def redo(self) -> bool:
        state = self._caretaker.redo(self._entries)
        if state is None:
            return False
        self._entries = state
        return True

    # Persistence with pandas
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([c.to_dict() for c in self._entries])

    def save_csv(self, path: str, encoding: str) -> str:
        df = self.to_dataframe()
        df.to_csv(path, index=False, encoding=encoding)
        return path

    def load_csv(self, path: str, encoding: str) -> int:
        try:
            df = pd.read_csv(path, encoding=encoding)
        except FileNotFoundError:
            raise ValidationError("History file not found")
        except Exception as e:
            raise ValidationError(f"Failed to read history: {e}")
        required = {"operation", "a", "b", "result", "timestamp"}
        if not required.issubset(df.columns):
            raise ValidationError("Malformed history CSV")
        self._entries = [Calculation.from_dict(row.to_dict()) for _, row in df.iterrows()]
        # Clear undo/redo stacks after load
        self._caretaker = Caretaker()
        return len(self._entries)
