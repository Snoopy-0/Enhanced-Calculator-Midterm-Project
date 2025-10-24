import copy
from typing import List
from .calculation import Calculation

class Memento:
    def __init__(self, state: List[Calculation]):
        # deep copy to freeze state
        self._state = copy.deepcopy(state)

    def get_state(self) -> List[Calculation]:
        return copy.deepcopy(self._state)

class Caretaker:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def push(self, m: Memento):
        self._undo_stack.append(m)
        self._redo_stack.clear()

    def undo(self, current_state) -> List[Calculation] | None:
        if not self._undo_stack:
            return None
        self._redo_stack.append(Memento(current_state))
        m = self._undo_stack.pop()
        return m.get_state()

    def redo(self, current_state) -> List[Calculation] | None:
        if not self._redo_stack:
            return None
        self._undo_stack.append(Memento(current_state))
        m = self._redo_stack.pop()
        return m.get_state()
