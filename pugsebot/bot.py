from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

from utils.logging import bot_logger
from utils.environment import TARGET_CHAT_ID, TOKEN, ENVIRONMENT_MODE, PORT

from commands import command_list

class PUGSEBot:
    logger = bot_logger
    chat_id = TARGET_CHAT_ID
    command_module_list = command_list

    def reply_text(self, **kwargs):
        update = kwargs['update']
        text = kwargs['response']
        if text:
            update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
            )
        return text

    def reply_photo(self, **kwargs):
        update = kwargs['update']
        photo = kwargs['response']
        if photo:
            update.message.reply_photo(photo=photo)
        return photo

    def send_text(self, **kwargs):
        text = kwargs['response']
        if text and self.chat_id:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
        return text

    def send_photo(self, **kwargs):
        photo = kwargs['response']
        if photo and self.chat_id:
            self.bot.send_photo(
                chat_id=self.chat_id,
                photo=photo,
            )
        return photo

    def __init__(self, bot_token):
        self.updater = Updater(bot_token, use_context=True)
        self.bot = self.updater.bot
        self.add_commands()

    def reply_with_command(self, bot_reply_func, create_content_func):
        def reply_content(update=None, context=None):
            return bot_reply_func(**create_content_func(update, context),)
        return reply_content

    def add_commands(self):
        text = 'Comandos aceitos: \n'
        # add commands
        self.dp = self.updater.dispatcher
        for command_module in self.command_module_list:
            command = command_module.name
            content_function = command_module.do_command
            reply_method = getattr(
                self,
                command_module.reply_function_name,
            )

            text += f'/{command}: {command_module.help_text}\n'
            self.dp.add_handler(
                CommandHandler(
                    command,
                    self.reply_with_command(
                        reply_method,
                        content_function,
                    ),
                ),
            )

        def help_command(update, context):
            return self.send_text(response=text)
        self.dp.add_handler(CommandHandler('help', help_command))

    def start(self):
        if ENVIRONMENT_MODE == 'PRODUCTION':
            app_name = 'pugse-telegram-bot'
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=TOKEN,
            )
            self.updater.bot.setWebhook(
                f'https://{app_name}.herokuapp.com/{TOKEN}',
            )
        else:
            self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    PUGSEBot(TOKEN).start()
