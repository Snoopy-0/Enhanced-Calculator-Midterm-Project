from app.calculation import Calculation

def test_calculation_roundtrip():
    c = Calculation.create("add", 2, 3, 5)
    d = c.to_dict()
    c2 = Calculation.from_dict(d)
    assert c2.operation == "add" and c2.a == 2 and c2.b == 3 and c2.result == 5
    assert "T" in c2.timestamp
