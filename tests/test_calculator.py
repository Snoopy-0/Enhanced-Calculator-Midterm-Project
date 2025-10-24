import os
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
        LOG_FILE=os.path.join(tmpdir, "calc.log"),
        HISTORY_FILE=os.path.join(tmpdir, "hist.csv"),
    )

def test_calculate_and_history(tmp_path):
    cfg = make_cfg(tmp_path)
    logger = get_logger(cfg)
    calc = Calculator(cfg, logger)
    r = calc.calculate("add", 2, 3)
    assert r == 5
    assert len(calc.history_list()) == 1

def test_undo_redo(tmp_path):
    cfg = make_cfg(tmp_path)
    logger = get_logger(cfg)
    calc = Calculator(cfg, logger)
    calc.calculate("add", 2, 2)
    calc.calculate("multiply", 3, 3)
    assert len(calc.history_list()) == 2
    assert calc.undo() is True
    assert len(calc.history_list()) == 1
    assert calc.redo() is True
    assert len(calc.history_list()) == 2

def test_save_load(tmp_path):
    cfg = make_cfg(tmp_path)
    logger = get_logger(cfg)
    calc = Calculator(cfg, logger)
    calc.calculate("percent", 25, 100)
    p = calc.save_history()
    assert os.path.exists(p)

    # new instance loads
    calc2 = Calculator(cfg, logger)
    cnt = calc2.load_history()
    assert cnt == 1
    hist = calc2.history_list()
    assert hist[0].operation == "percent" and hist[0].result == 25
