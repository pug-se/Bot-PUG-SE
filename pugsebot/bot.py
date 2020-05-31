import logging
import os

from telegram.ext import Updater, CommandHandler

import utils
from functions import start, send, news, udemy, memes, about

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

token = os.environ['TELEGRAM_KEY']

class PUGSEBot():
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    logger = logging.getLogger('PUGSEBot')

    def reply_message(self, update, context, text):
        person_name = update.effective_user.full_name
        if not text:
            text = "Ocorreu algum problema e não consegui atender seu pedido."
        text = f"{person_name}, " + text
        update.message.reply_text(text)

    @staticmethod
    def reply_image(update, context, image):
        update.message.reply_photo(photo=image)

    def send_message(self, text):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
        )

    def send_image(self, url):
        self.bot.send_photo(
            chat_id=self.chat_id,
            photo=url,
        )

    def init_schedules(self):
        memes.schedule(
            self.schedule_manager,
            self.send_image,
            UM_DIA_EM_SEGUNDOS,
        )
        udemy.schedule(
            self.schedule_manager,
            self.send_message,
            UM_DIA_EM_SEGUNDOS / 4,
        )
        news.schedule(
            self.schedule_manager,
            self.send_message,
            UM_DIA_EM_SEGUNDOS * 2,
        )

    def __init__(self):
        self.updater = Updater(token=token, use_context=True)
        self.schedule_manager = utils.ScheduleManager()
        self.bot = self.updater.bot
        self.dp = self.updater.dispatcher
        self.dp.add_handler(
            CommandHandler('start', start.reply(self.reply_message))
        )
        self.dp.add_handler(
            CommandHandler('send', send.reply(self.send_message))
        )
        self.dp.add_handler(
            CommandHandler('news', news.reply(self.reply_message))
        )
        self.dp.add_handler(
            CommandHandler('udemy', udemy.reply(self.reply_message))
        )
        self.dp.add_handler(
            CommandHandler('memes', memes.reply(self.reply_image))
        )
        self.dp.add_handler(
            CommandHandler('about', about.reply(self.reply_message))
        )
        self.updater.start_polling()
        self.init_schedules()
        self.updater.idle()

if __name__ == "__main__":
    PUGSEBot()
