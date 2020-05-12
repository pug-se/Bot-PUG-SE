import logging
import os

from telegram.ext import Updater, CommandHandler

import utils
from memes import get_random_meme_image

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token = os.environ["TELEGRAM_KEY"]


class PUGSEBot:
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    logger = logging.getLogger("PUGSEBot")

    def start(self, update, context):
        text = "olá, sou o PUG-SE-BOT teste."
        self.reply_message(update, context, text)

    def get_udemy_coupons(self, update=None, context=None):
        text = ""
        try:
            url = "https://couponscorpion.com/"
            soup = utils.get_html_soup(url)
            title_list = []
            url_list = []
            for h3 in soup.findAll("h3"):
                a = h3.find("a")
                if a:
                    title_list.append(a.text.strip())
                    url_list.append(a.get("href").strip())

            text = "esses foram os cupons da Udemy que encontrei:\n"

            for _, url in zip(title_list, url_list):
                text += f"{url} \n"

        except Exception as e:
            self.logger.error(e)

        if update is not None and context is not None:
            self.reply_message(update, context, text)
        else:
            self.send_text(text)

    def get_python_news(self, update=None, context=None):
        text = ""
        try:
            url = "https://www.python.org/blogs/"
            soup = utils.get_html_soup(url)

            h3 = soup.find("h3", {"class": "event-title"})
            a = h3.find("a")
            title = a.text.strip()
            url = a.get("href").strip()
            text = f"a notícia mais quente sobre Python:\n{title} — {url}"
        except Exception as e:
            self.logger.error(e)

        if update is not None and context is not None:
            self.reply_message(update, context, text)
        else:
            self.send_text(text)

    def reply_message(self, update, context, text):
        person_name = update.effective_user.full_name
        if not text:
            text = "Ocorreu algum problema e não consegui atender seu pedido."
        text = f"{person_name}, " + text
        update.message.reply_text(text)

    @staticmethod
    def reply_meme(update, context):
        update.message.reply_photo(photo=get_random_meme_image())

    def send_message(self, update, context):
        text = update.message.text.replace("/send", "")
        context.bot.send_message(chat_id=self.chat_id, text=text)

    def send_text(self, text):
        self.bot.send_message(chat_id=self.chat_id, text=text)

    def send_image(self, url):
        self.bot.send_photo(chat_id=self.chat_id, photo=url)

    def send_memes(self):
        def send_meme():
            self.send_image(get_random_meme_image())

        self.schedule_manager.add_schedule(send_meme, UM_DIA_EM_SEGUNDOS)

    def about(self, update, context):
        text = "Este bot foi feito pela comunidade de python PUG-SE para levar informações importantes sobre a linguagem python e eventos da comunidade.\nPara saber quais as funcionalidades do bot digite /help \nPara saber mais ou contribbuir com o projeto: https://github.com/pug-se/Bot-PUG-SE"
        self.reply_message(update, context, text)

    def init_schedules(self):
        self.send_memes()
        self.schedule_manager.add_schedule(
            self.get_udemy_coupons, UM_DIA_EM_SEGUNDOS / 4
        )
        self.schedule_manager.add_schedule(self.get_python_news, UM_DIA_EM_SEGUNDOS * 2)

    def __init__(self):
        self.updater = Updater(token=token, use_context=True)
        self.schedule_manager = utils.ScheduleManager()
        self.bot = self.updater.bot
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("send", self.send_message))
        self.dp.add_handler(CommandHandler("news", self.get_python_news))
        self.dp.add_handler(CommandHandler("udemy", self.get_udemy_coupons))
        self.dp.add_handler(CommandHandler("memes", self.reply_meme))
        self.dp.add_handler(CommandHandler("about", self.about))
        self.updater.start_polling()
        self.init_schedules()
        self.updater.idle()


if __name__ == "__main__":
    PUGSEBot()
