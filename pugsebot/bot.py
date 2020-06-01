import logging
import os

from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

import threading

import utils
from memes import get_random_meme_image

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token = os.environ["TELEGRAM_KEY"]
target_chat_id = os.environ["TELEGRAM_CHAT_ID"]
environment = os.environ.get('ENVIRONMENT', None)
port = os.environ.get('PORT', None)

class PUGSEBot:
    logger = logging.getLogger("PUGSEBot")
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

    def send_photo(self, photo_url):
        if photo_url and self.chat_id:
            self.bot.send_photo(
                chat_id=self.chat_id, 
                photo=photo_url,
            )
        return photo_url

    def say(self, update=None, context=None):
        if update:
            text = update.message.text.replace("/say", "")
            if text:
                self.send_text(text=text)
        return update

    def get_about(self, update=None, context=None):
        text = "Este bot foi feito pela comunidade de Python PUG-SE para levar informações importantes sobre a linguagem Python e eventos da comunidade.\nPara saber quais as funcionalidades do bot digite /help \nPara saber mais ou contribuir com o projeto: https://github.com/pug-se/Bot-PUG-SE"
        if update:
            return self.reply_text(update, text)
        return text

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

            text = "Esses foram os cupons da Udemy que encontrei:\n\n"

            i = 1
            for title, url in zip(title_list, url_list):
                text += f'{i}) <a href="{url}">{title}</a>\n'
                i += 1

        except Exception as e:
            self.logger.error(e)

        if update is not None:
            return self.reply_text(update, text)
        else:
            return self.send_text(text)

    def get_python_news(self, update=None, context=None):
        text = ""
        try:
            url = "https://www.python.org/blogs/"
            soup = utils.get_html_soup(url)

            h3 = soup.find("h3", {"class": "event-title"})
            a = h3.find("a")
            title = a.text.strip()
            url = a.get("href").strip()
            text = 'A notícia mais quente sobre Python:\n'
            text += f'<a href="{url}">{title}</a>'
        except Exception as e:
            self.logger.error(e)

        if update is not None:
            return self.reply_text(update, text)
        else:
            return self.send_text(text)

    def get_memes(self, update=None, context=None):
        if update is not None and context is not None:
            return self.reply_photo(update, get_random_meme_image())
        else:
            return self.send_photo(get_random_meme_image())

    def get_projects(self, update=None, context=None):
        repo_url = 'http://api.github.com/orgs/pug-se/repos'
        text = 'Os projetos da comunidade estão no '
        text += f'<a href="{repo_url}">GitHub</a>\n\n'
        
        url = 'https://api.github.com/orgs/pug-se/repos'
        info_dict = utils.get_json(url)
        i = 1
        for info in info_dict:
            name = info['name']
            description = info['description']
            url = info['html_url']
            text += f'{i})  <a href="{url}">{name}</a>: {description}\n'
            i += 1
        if update is not None:
            return self.reply_text(update, text)
        return text
    
    def add_schedules(self):
        self.schedule_manager.add_schedule(
            self.get_memes, 
            UM_DIA_EM_SEGUNDOS,
        )
        self.schedule_manager.add_schedule(
            self.get_udemy_coupons, 
            UM_DIA_EM_SEGUNDOS / 4,
        )
        self.schedule_manager.add_schedule(
            self.get_python_news, 
            UM_DIA_EM_SEGUNDOS * 2,
        )
    
    def __init__(self):
        self.updater = Updater(token=token, use_context=True)
        self.schedule_manager = utils.ScheduleManager()
        self.bot = self.updater.bot
        # add commands
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("say", self.say))
        self.dp.add_handler(CommandHandler("news", self.get_python_news))
        self.dp.add_handler(CommandHandler("udemy", self.get_udemy_coupons))
        self.dp.add_handler(CommandHandler("memes", self.get_memes))
        self.dp.add_handler(CommandHandler("about", self.get_about))
        self.dp.add_handler(CommandHandler("projects", self.get_projects))

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