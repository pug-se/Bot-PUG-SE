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

ENVIRONMENT_MODE = os.environ.get('ENVIRONMENT', None)
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///local_db.sqlite'
TOKEN = os.environ['TELEGRAM_KEY']
TARGET_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PORT = os.environ.get('PORT', None)
