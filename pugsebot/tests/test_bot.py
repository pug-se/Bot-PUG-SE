"""Test bot functionalities."""

import unittest
from unittest.mock import Mock, patch

from telegram.update import Update
from telegram import ParseMode

from ..bot import PUGSEBot, TOKEN, PORT
from .. import utils


class TestBot(unittest.TestCase):
    """Test bot functionalities."""

    def test_add_commands(self):
        """Test add_commands."""
        bot = PUGSEBot(TOKEN)

        handler_list = bot.dp.handlers[0]
        command_list = utils.command.get_commands()
        self.assertEqual(len(handler_list), len(command_list))
        name_list1 = [command.name for command in command_list]
        name_list2 = []
        for handler in handler_list:
            name_list2.append(handler.command[0])
        self.assertEqual(set(name_list1), set(name_list2))

    def test_reply_text(self):
        bot = PUGSEBot(TOKEN)
        update = Mock(spec=Update(0))
        text = "test"
        result = bot.reply_text(response=text, update=update)
        update.message.reply_text.assert_called_with(
            text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        self.assertEqual(result, text)

    def test_reply_photo(self):
        bot = PUGSEBot(TOKEN)
        update = Mock(spec=Update(0))
        photo = "test"
        result = bot.reply_photo(response=photo, update=update)
        update.message.reply_photo.assert_called_with(photo=photo)
        self.assertEqual(result, photo)

    def test_send_text(self):
        bot = PUGSEBot(TOKEN)
        bot.bot.send_message = Mock()
        text = "test"
        result = bot.send_text(response=text)
        bot.bot.send_message.assert_called_with(
            chat_id=bot.chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        self.assertEqual(result, text)

    def test_send_photo(self):
        bot = PUGSEBot(TOKEN)
        bot.bot.send_photo = Mock()
        photo = "test"
        result = bot.send_photo(response=photo)
        bot.bot.send_photo.assert_called_with(
            chat_id=bot.chat_id, photo=photo,
        )
        self.assertEqual(result, photo)
        return photo

    @patch("pugsebot.bot.Updater")
    @patch("pugsebot.bot.PUGSEBot.add_commands")
    def test_init(self, add_commands, Updater):
        bot = PUGSEBot(TOKEN)
        add_commands.assert_called()
        Updater.assert_called_with(TOKEN, use_context=True)

    @patch("pugsebot.bot.ENVIRONMENT_MODE", "PRODUCTION")
    def test_start_production(self):
        bot = PUGSEBot(TOKEN)
        bot.updater = Mock()
        bot.start(block=False)
        bot.updater.start_webhook.assert_called_with(
            listen="0.0.0.0", port=PORT, url_path=TOKEN,
        )
        bot.updater.bot.setWebhook.assert_called_with(
            f"https://{bot.app_name}.herokuapp.com/{TOKEN}"
        )
