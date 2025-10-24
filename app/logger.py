import logging
from .calculator_config import Config

_LOGGER = None

def get_logger(cfg: Config) -> logging.Logger:
    global _LOGGER
    if _LOGGER:
        return _LOGGER
    logger = logging.getLogger("advanced_calculator")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(cfg.LOG_FILE, encoding=cfg.DEFAULT_ENCODING)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    _LOGGER = logger
    return logger
