"""Test bot functionalities."""

import unittest

import bot
import utils

"""
testes de integração também
funções separadas
"""


class TestBot(unittest.TestCase):
    """Test bot functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the bot and chat id."""
        cls.bot = bot.PUGSEBot(utils.environment.TOKEN)
        cls.bot.chat_id = None

    def test_add_commands(self):
        """Test add_commands."""
        handler_list = self.bot.dp.handlers[0]
        command_list = utils.command.get_commands()
        self.assertEqual(len(handler_list), len(command_list))
        name_list1 = [command.name for command in command_list]
        name_list2 = []
        for handler in handler_list:
            name_list2.append(handler.command[0])
        self.assertEqual(set(name_list1), set(name_list2))
