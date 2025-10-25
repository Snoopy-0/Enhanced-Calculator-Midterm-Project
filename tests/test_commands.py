from app.calculator import Calculator
from app.calculator_config import Config
from app.logger import get_logger
from app.commands import CommandFactory

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

def test_command_add_and_history(tmp_path):
    cfg = make_cfg(tmp_path)
    calc = Calculator(cfg, get_logger(cfg))
    cf = CommandFactory(calc)

    ok, msg = cf.execute("add", ["3", "5"])
    assert ok and "Result:" in msg

    ok, msg = cf.execute("history", [])
    assert ok and "add(3.0, 5.0)" in msg

def test_clear_undo_redo_save_load(tmp_path):
    cfg = make_cfg(tmp_path)
    calc = Calculator(cfg, get_logger(cfg))
    cf = CommandFactory(calc)

    cf.execute("add", ["2", "2"])
    cf.execute("multiply", ["3", "3"])

    ok, msg = cf.execute("undo", [])
    assert ok and "Undone" in msg

    ok, msg = cf.execute("redo", [])
    assert ok and "Redid" in msg

    ok, msg = cf.execute("save", [])
    assert ok and "History saved to" in msg

    # new instance loads the same file (exercise load path)
    calc2 = Calculator(cfg, get_logger(cfg))
    cf2 = CommandFactory(calc2)
    ok, msg = cf2.execute("load", [])
    assert ok and "Loaded" in msg

def test_unknown_command(tmp_path):
    cfg = make_cfg(tmp_path)
    calc = Calculator(cfg, get_logger(cfg))
    cf = CommandFactory(calc)
    ok, msg = cf.execute("woot", [])
    assert ok is False and "Unknown command" in msg
