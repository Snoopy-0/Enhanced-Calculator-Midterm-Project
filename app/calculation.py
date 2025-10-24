from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @staticmethod
    def create(operation: str, a: float, b: float, result: float) -> "Calculation":
        ts = datetime.utcnow().isoformat()
        return Calculation(operation, a, b, result, ts)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Calculation":
        return Calculation(d["operation"], float(d["a"]), float(d["b"]), float(d["result"]), d["timestamp"])
