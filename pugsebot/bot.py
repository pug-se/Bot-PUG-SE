from telegram.ext import Updater, CommandHandler

import logging
import os 

import utils
from memes import get_url_image_vida_programador

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token = os.environ['TELEGRAM_KEY']

class PUGSEBot():
    chatId = "-1001413864839" # trocar para o id do grupo PUGSE
    logger = logging.getLogger('PUGSEBot')
    
    def start(self, update, context):
        text = "Olá, Sou o PUG-SE-BOT teste."
        self.reply_message(update, context, text)

    def get_udemy_coupons(self, update, context):
        text = ''
        try:
            url = 'https://couponscorpion.com/'
            soup = utils.get_html_soup(url)
            title_list = []
            url_list = []
            for h3 in soup.findAll('h3'):
                a = h3.find('a')
                if a:
                    title_list.append(a.text.strip())
                    url_list.append(a.get('href').strip())
            
            text = "esses foram os cupons da Udemy que encontrei:\n"

            for _, url in zip(title_list, url_list):           
                text += f'{url} \n'

        except Exception as e:
            self.logger.error(e)

        self.reply_message(update, context, text)

    def get_python_news(self, update, context):
        text = ''
        try:
            url = 'https://www.python.org/blogs/'
            soup = utils.get_html_soup(url)
            
            h3 = soup.find('h3',{'class':'event-title'})
            a = h3.find('a')
            title = a.text.strip()
            url = a.get('href').strip()
            text = f'a notícia mais quente sobre Python:\n{title} — {url}'
        except Exception as e:
            self.logger.error(e)

        self.reply_message(update, context, text)

    def reply_message(self, update, context, text):
        person_name = update.effective_user.full_name
        if not text:
            text = "Ocorreu algum problema e não consegui atender seu pedido."
        text = f"{person_name}, " + text
        update.message.reply_text(text)

    def send_message(self, update, context):
        text = update.message.text.replace('/send','')
        context.bot.send_message(
            chat_id=self.chatId,
            text=text)

    def send_image(self, context, url):
        context.bot.send_photo(
            chat_id=self.chatId,
            photo=url,
        )

    def send_memes(self, update, context):
        def send_meme():
            self.send_image(context, get_url_image_vida_programador())

        self.schedule_manager.add_schedule(send_meme)
        self.schedule_manager.start_schedules()

    def __init__(self):
        self.updater = Updater(token=token, use_context=True)
        self.schedule_manager = utils.ScheduleManager()
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("send", self.send_message))
        self.dp.add_handler(CommandHandler("news", self.get_python_news))
        self.dp.add_handler(CommandHandler("udemy", self.get_udemy_coupons))
        self.dp.add_handler(CommandHandler("udemy", self.get_udemy_coupons))
        self.dp.add_handler(CommandHandler('memes', self.send_memes))
        self.updater.start_polling()
        self.updater.idle()
    
if __name__ == "__main__":
    PUGSEBot()
