import pandas as pd
import pytest
from app.history import History
from app.exceptions import ValidationError

def test_load_missing_file(tmp_path):
    h = History(10)
    with pytest.raises(ValidationError):
        h.load_csv(str(tmp_path / "nope.csv"), "utf-8")

def test_load_malformed_csv(tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"foo":[1]}).to_csv(bad, index=False)
    h = History(10)
    with pytest.raises(ValidationError):
        h.load_csv(str(bad), "utf-8")
