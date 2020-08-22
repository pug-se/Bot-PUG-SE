"""Test bot functionalities."""

# fazer testes de integração para ambos

import unittest

import bot
import utils

from utils import schedule_manager


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
        command_list = utils.command_modules.get_commands()
        self.assertEqual(len(handler_list), len(command_list))
        name_list1 = [command.name for command in command_list]
        name_list2 = []
        for handler in handler_list:
            name_list2.append(handler.command[0])
        self.assertEqual(set(name_list1), set(name_list2))


class TestSchedules(unittest.TestCase):
    """Test run_schedules module."""

    def test_get_schedule_list(self):
        """Test get_schedule_list."""
        schedules = schedule_manager.get_schedule_list()
        bot_commands = utils.command_modules.get_commands()
        schedules_count = 0
        for bot_command in bot_commands:
            if bot_command.get_schedule():
                schedules_count += 1

        self.assertEqual(schedules_count, len(schedules))
