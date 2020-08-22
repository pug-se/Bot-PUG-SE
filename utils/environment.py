"""Loads environment variables.

Variables:

ENVIRONMENT_MODE:
    Defines the environment as Development or Production
DATABASE_URL:
    Uses the format defined by SQLAlchemy
TOKEN:
    Bot Telegram token
PORT:
    Port used by the bot at Production mode
"""

import os

import sys


default_db_url = "sqlite:///local_db.sqlite"


def get_database_url():
    db_url_env = os.environ.get("DATABASE_URL", None)
    if "pytest" in sys.modules or not db_url_env:
        return default_db_url
    return db_url_env


ENVIRONMENT_MODE = os.environ.get("ENVIRONMENT", None)
DATABASE_URL = get_database_url()
TOKEN = os.environ["TELEGRAM_KEY"]
TARGET_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
PORT = os.environ.get("PORT", None)
