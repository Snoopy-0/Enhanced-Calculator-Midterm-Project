from app.calculator_config import load_config

def test_load_config_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "hist"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    cfg = load_config()
    assert cfg.LOG_DIR.endswith("logs")
    assert cfg.HISTORY_DIR.endswith("hist")
    assert cfg.AUTO_SAVE is False
    assert (tmp_path / "logs").exists()
    assert (tmp_path / "hist").exists()
