"""Main module for starting and running bot."""

from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

from .utils.logging import bot_logger
from .utils.environment import TARGET_CHAT_ID, TOKEN, ENVIRONMENT_MODE, PORT
from .utils.command import get_commands


class PUGSEBot:
    """
    A wrapper for all bot related stuff.

    Defines utility response methods and binds:
        * the python-telegram-bot Updater object
        * the python-telegram-bot Bot object
        * commands found by utils.module

    Attributes:
        logger:
            Logger defined in utils.logging
        chat_id:
            Telegram chat id in which the bot is a member
    """

    logger = bot_logger
    chat_id = TARGET_CHAT_ID
    app_name = "pugse-telegram-bot"  # Heroku app name

    def reply_text(self, **kwargs):
        """Reply a text message with HTML parsing.

        Arguments:
        update:
            python-telegram-bot Update object
        response:
            message returned by a command function
        """
        update = kwargs["update"]
        text = kwargs["response"]
        if text:
            update.message.reply_text(
                text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )
        return text

    def reply_photo(self, **kwargs):
        """Reply a image message.

        Arguments:
        update:
            python-telegram-bot Update object
        response:
            image url returned by a command function
        """
        update = kwargs["update"]
        photo = kwargs["response"]
        if photo:
            update.message.reply_photo(photo=photo)
        return photo

    def send_text(self, **kwargs):
        """Send a text message to the group pointed by chat_id.

        Arguments:
        response:
            message returned by a command function
        """
        text = kwargs["response"]

        if text:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        return text

    def send_photo(self, **kwargs):
        """Send a image message to the group pointed by chat_id.

        Arguments:
        response:
            image url returned by a command function
        """
        photo = kwargs["response"]
        if photo:
            self.bot.send_photo(
                chat_id=self.chat_id, photo=photo,
            )
        return photo

    def __init__(self, bot_token):
        """Bind the wrapper with python-telegram-bot objects."""
        self.updater = Updater(bot_token, use_context=True)
        self.bot = self.updater.bot
        self.add_commands()

    def add_commands(self):
        """Bind commands found by utils.module.get_commands."""

        def reply_with_command(bot_reply_func, create_content_func):
            def reply_content(update=None, context=None):
                return bot_reply_func(**create_content_func(update, context))

            return reply_content

        self.dp = self.updater.dispatcher
        command_module_list = get_commands()
        for command_module in command_module_list:
            command = command_module.name
            content_function = command_module.do_command
            reply_method = getattr(self, command_module.reply_function_name,)

            self.dp.add_handler(
                CommandHandler(
                    command,
                    reply_with_command(reply_method, content_function,),
                ),
            )

    def start(self, block=True):
        """Run the bot at development mode (default) or production mode.

        Mode is defined by an Environment Variable
         collected at utils.environment.ENVIRONMENT_MODE
        """
        if ENVIRONMENT_MODE == "PRODUCTION":
            self.updater.start_webhook(
                listen="0.0.0.0", port=PORT, url_path=TOKEN,
            )
            self.updater.bot.setWebhook(
                f"https://{self.app_name}.herokuapp.com/{TOKEN}",
            )
        elif block:
            self.updater.start_polling()
        if block:
            self.updater.idle()


if __name__ == "__main__":
    PUGSEBot(TOKEN).start()
