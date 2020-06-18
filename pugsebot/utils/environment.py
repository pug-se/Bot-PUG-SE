import os

ENVIRONMENT_MODE = os.environ.get('ENVIRONMENT', None)
DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///local_db.sqlite'
TOKEN = os.environ['TELEGRAM_KEY']
TARGET_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
PORT = os.environ.get('PORT', None)
