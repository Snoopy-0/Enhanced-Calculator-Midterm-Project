from unittest.mock import Mock
from app.calculator import Calculator
from app.calculator_config import Config
from app.logger import get_logger
import os

class DummyCfg(Config): pass

def make_cfg(tmpdir, autosave=False):
    return DummyCfg(
        LOG_DIR=str(tmpdir),
        HISTORY_DIR=str(tmpdir),
        MAX_HISTORY_SIZE=10,
        AUTO_SAVE=autosave,
        PRECISION=6,
        MAX_INPUT_VALUE=1e6,
        DEFAULT_ENCODING="utf-8",
        LOG_FILE=str(tmpdir / "calc.log"),
        HISTORY_FILE=str(tmpdir / "hist.csv"),
    )

def test_observer_notified(tmp_path):
    cfg = make_cfg(tmp_path)
    calc = Calculator(cfg, get_logger(cfg))
    mock_obs = Mock()
    calc.observers = [mock_obs]

    calc.calculate("add", 1, 2)
    mock_obs.update.assert_called_once()
    args, _ = mock_obs.update.call_args
    assert args[0].operation == "add" and args[0].result == 3

def test_autosave_on(tmp_path):
    cfg = make_cfg(tmp_path, autosave=True)
    calc = Calculator(cfg, get_logger(cfg))
    calc.calculate("add", 1, 2)
    assert os.path.exists(cfg.HISTORY_FILE)
