import pytest
from app.operations import OperationFactory

@pytest.mark.parametrize("op,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 10, 4, 6),
    ("multiply", 3, 4, 12),
    ("divide", 8, 2, 4),
    ("power", 2, 3, 8),
    ("root", 9, 2, 3),
    ("modulus", 10, 3, 1),
    ("int_divide", 10, 3, 3),
    ("percent", 25, 100, 25),
    ("abs_diff", 5, 12, 7),
])
def test_operations(op, a, b, expected):
    fn = OperationFactory.create(op)
    assert fn.execute(a, b) == pytest.approx(expected)

def test_divide_by_zero():
    with pytest.raises(Exception):
        OperationFactory.create("divide").execute(1, 0)

def test_unknown_operation():
    with pytest.raises(Exception):
        OperationFactory.create("nope")
