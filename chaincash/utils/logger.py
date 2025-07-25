import sys
from loguru import logger

logger.remove()

logger.add(
    sink     = sys.stdout,
    format   = (
        "<white>{time:HH:mm:ss}</white>"
        " | <level>{level: <8}</level>"
        " | <cyan><b>{file}</b></cyan>:<cyan><b>{line}</b></cyan>"
        " - <white><b>{message}</b></white>"
    ),
    colorize = True,
    level    = "INFO",
    enqueue  = True
)