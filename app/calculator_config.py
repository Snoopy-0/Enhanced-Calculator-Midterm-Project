import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    LOG_DIR: str
    HISTORY_DIR: str
    MAX_HISTORY_SIZE: int
    AUTO_SAVE: bool
    PRECISION: int
    MAX_INPUT_VALUE: float
    DEFAULT_ENCODING: str
    LOG_FILE: str
    HISTORY_FILE: str

def load_config() -> Config:
    load_dotenv()
    log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs")
    hist_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history")
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(hist_dir, exist_ok=True)
    cfg = Config(
        LOG_DIR=log_dir,
        HISTORY_DIR=hist_dir,
        MAX_HISTORY_SIZE=int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000")),
        AUTO_SAVE=os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true",
        PRECISION=int(os.getenv("CALCULATOR_PRECISION", "6")),
        MAX_INPUT_VALUE=float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e12")),
        DEFAULT_ENCODING=os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"),
        LOG_FILE=os.path.join(log_dir, os.getenv("CALCULATOR_LOG_FILE", "calculator.log")),
        HISTORY_FILE=os.path.join(hist_dir, os.getenv("CALCULATOR_HISTORY_FILE", "history.csv"))
    )
    return cfg
