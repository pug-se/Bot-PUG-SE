"""Define utilites for logging."""

import logging
import sys

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

cache_logger = logging.getLogger('cache')
bot_logger = logging.getLogger('Bot')
command_logger = logging.getLogger('Command')
schedule_logger = logging.getLogger('apscheduler.scheduler')

logger_list = [
    cache_logger, bot_logger,
    command_logger, schedule_logger
]

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

for logger in logger_list:
    logger.addHandler(handler)

def set_level(level):
    """Set a level to all loggers."""
    for logger in logger_list:
        logger.setLevel(level)
