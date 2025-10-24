from unittest.mock import Mock
from app.calculator import Calculator
from app.calculator_config import Config
from app.logger import get_logger

class DummyCfg(Config): pass

def make_cfg(tmpdir):
    return DummyCfg(
        LOG_DIR=str(tmpdir),
        HISTORY_DIR=str(tmpdir),
        MAX_HISTORY_SIZE=100,
        AUTO_SAVE=False,
        PRECISION=6,
        MAX_INPUT_VALUE=1e6,
        DEFAULT_ENCODING="utf-8",
        LOG_FILE=str(tmpdir / "calc.log"),
        HISTORY_FILE=str(tmpdir / "hist.csv"),
    )

def test_observer_notified(tmp_path):
    cfg = make_cfg(tmp_path)
    logger = get_logger(cfg)
    calc = Calculator(cfg, logger)

    # Replace observers with a mock
    mock_obs = Mock()
    calc.observers = [mock_obs]

    calc.calculate("add", 1, 2)
    assert len(calc.history_list()) == 1
    # Verify observer called once with a Calculation
    mock_obs.update.assert_called_once()
    args, _ = mock_obs.update.call_args
    assert args[0].operation == "add"
    assert args[0].result == 3
