import logging
from logging.handlers import RotatingFileHandler

from pythonjsonlogger.json import JsonFormatter

ROOT_LOGGER = logging.getLogger()
logHandler = RotatingFileHandler(
    filename="logs/liceo.log", maxBytes=1024, backupCount=3
)
formatter = JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s %(exc_info)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logHandler.setFormatter(formatter)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
ROOT_LOGGER.addHandler(logHandler)


# --8<-- [start:logged]
def logged(path: str):
    class Logged:
        _logger = logging.getLogger(path)

    return Logged


# --8<-- [end:logged]
