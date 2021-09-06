import logging
import sys
from pathlib import Path

log_dir = Path(__file__).parent / "logs"

if not log_dir.is_dir():
    log_dir.mkdir()


logging.basicConfig(
    filename=str(log_dir / "daily_record.log"),
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("__name__")
logger.addHandler(logging.StreamHandler(sys.stdout))

logFormatter = logging.Formatter(
    "%(asctime)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

fileHandler = logging.FileHandler(str(log_dir / "daily_record.log"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
