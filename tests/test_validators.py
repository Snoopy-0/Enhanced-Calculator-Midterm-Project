import pytest
from app.input_validators import parse_two_numbers
from app.calculator_config import Config
from app.exceptions import ValidationError

class DummyCfg(Config): pass

def make_cfg():
    return DummyCfg("","",10,False,6,10,"utf-8","","")

def test_parse_two_numbers_ok():
    a, b = parse_two_numbers(["3","4"], make_cfg())
    assert a == 3 and b == 4

@pytest.mark.parametrize("args", [[], ["3"], ["3","x"], ["3","4","5"]])
def test_parse_two_numbers_errors(args):
    with pytest.raises(ValidationError):
        parse_two_numbers(args, make_cfg())

def test_parse_two_numbers_max_exceeded():
    with pytest.raises(ValidationError):
        parse_two_numbers(["11","0"], make_cfg())
