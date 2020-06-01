import logging
import os

from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

import utils
from functions import say, news, udemy, memes, about, projects

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

token = os.environ['TELEGRAM_KEY']
target_chat_id = os.environ['TELEGRAM_CHAT_ID']
environment = os.environ.get('ENVIRONMENT', None)
port = os.environ.get('PORT', None)

class PUGSEBot:
    logger = logging.getLogger('PUGSEBot')
    chat_id = target_chat_id

    def reply_text(self, update, text):
        if text:
            update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
            )
        return text

    def reply_photo(self, update, photo):
        if photo:
            update.message.reply_photo(photo=photo)
        return photo

    def send_text(self, text):
        if text and self.chat_id:
            self.bot.send_message(
                chat_id=self.chat_id, 
                text=text,
                parse_mode=ParseMode.HTML,
            )
        return text

    def send_photo(self, photo):
        if photo and self.chat_id:
            self.bot.send_photo(
                chat_id=self.chat_id, 
                photo=photo,
            )
        return photo

    def add_schedules(self):
        memes.schedule(
            self.schedule_manager,
            self.send_photo,
            UM_DIA_EM_SEGUNDOS,
        )
        udemy.schedule(
            self.schedule_manager,
            self.send_text,
            UM_DIA_EM_SEGUNDOS / 4,
        )
        news.schedule(
            self.schedule_manager,
            self.send_text,
            UM_DIA_EM_SEGUNDOS * 2,
        )

    def __init__(self):
        self.updater = Updater(token=token, use_context=True)
        self.schedule_manager = utils.ScheduleManager()
        self.bot = self.updater.bot
        # add commands
        self.dp = self.updater.dispatcher
        self.dp.add_handler(
            CommandHandler('say', say.reply(self.send_text))
        )
        self.dp.add_handler(
            CommandHandler('news', news.reply(self.reply_text))
        )
        self.dp.add_handler(
            CommandHandler('udemy', udemy.reply(self.reply_text))
        )
        self.dp.add_handler(
            CommandHandler('memes', memes.reply(self.reply_photo))
        )
        self.dp.add_handler(
            CommandHandler('about', about.reply(self.reply_text))
        )
        self.dp.add_handler(
            CommandHandler('projects', projects.reply(self.reply_text))
        )

    def start(self):
        #self.add_schedules()

        if environment == 'PRODUCTION':
            app_name = 'pugse-telegram-bot'
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=token,
            )
            self.updater.bot.setWebhook(
                f'https://{app_name}.herokuapp.com/{token}',
            )
        else:
            self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    PUGSEBot().start()
