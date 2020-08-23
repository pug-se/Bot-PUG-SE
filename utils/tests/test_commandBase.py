import unittest
from unittest.mock import Mock, patch

from utils import database, schedule, command_base


class TestCommandBase(unittest.TestCase):
    """Test CommandBase functionalities."""

    @classmethod
    def setUpClass(cls):
        """Mock a command."""
        cls.message = "test"
        cls.name = "test"
        cls.help_text = "test"
        cls.reply_function_name = "reply_text"

        class MockCommand(command_base.CommandBase):
            def __init__(self, interval=None, expire=None):
                super().__init__(
                    name=cls.name,
                    help_text=cls.help_text,
                    reply_function_name=cls.reply_function_name,
                    schedule_interval=interval,
                    expire=expire,
                )

            def function(self, update=None, context=None):
                return cls.message

        cls.Command = MockCommand

    @patch("utils.command_base.CommandInfo")
    def test_set_info(self, CommandInfo):
        """Test set_info."""
        text = "test"
        command = self.Command()
        command.set_info(self.message, text)
        CommandInfo.set_value.assert_called_with(self.name, self.message, text)

    @patch("utils.command_base.CommandInfo.get_value")
    def test_get_info(self, get_value):
        """Test get_info."""
        data_dict = {}
        get_value.return_value = data_dict.get("test")

        command = self.Command()
        info = command.get_info(self.message)
        self.assertIsNone(info)

        text = "test"
        data_mock = Mock()
        data_mock.info = text
        get_value.return_value = data_mock

        info = command.get_info(self.message)
        self.assertEqual(info, text)

    @patch("utils.command_base.CommandInfo.remove_value")
    def test_remove_info(self, remove_value):
        """Test remove_info."""
        command = self.Command()
        removed = command.remove_info(self.message)
        remove_value.assert_called_with(self.name, self.message)

    @patch("utils.command_base.Cache")
    def test_get_result(self, Cache):
        """Test get_result with cached results."""
        expire = 3
        command = self.Command(expire=expire)

        Cache.get_value.return_value = None
        cached_item = Mock()
        cached_item.result = command.function()
        Cache.set_value.return_value = cached_item

        result = command.get_result()
        Cache.get_value.assert_called_with(self.name)
        self.assertEqual(result, command.function())

        cached_item.result = "test2"
        Cache.get_value.return_value = cached_item
        result = command.get_result()
        Cache.get_value.assert_called_with(self.name)
        self.assertNotEqual(result, command.function())
        self.assertEqual(result, cached_item.result)

    def test_get_schedule(self):
        """Test get_schedule."""
        command = self.Command()
        sched = command.get_schedule()
        self.assertIsNone(sched)

        command_sched = self.Command(5)
        sched = command_sched.get_schedule()
        self.assertTrue(isinstance(sched, schedule.Schedule))

    def test_function_not_implemented(self):
        """Test CommandBase function."""
        with self.assertRaises(NotImplementedError):
            command_base.CommandBase(None, None, None, None).function()

    def test_function(self):
        """Test function."""
        self.assertEqual(self.Command().function(), self.message)

    def test_init(self):
        """Test initialization."""
        command = self.Command()
        self.assertEqual(command.name, self.name)
        self.assertEqual(command.help_text, self.help_text)
        self.assertEqual(
            command.reply_function_name, self.reply_function_name,
        )

        interval = 1
        expire = 1
        command = self.Command(interval, expire)
        self.assertEqual(command.interval, interval)
        self.assertEqual(command.expire, expire)

    def test_do_command(self):
        """Test do_command."""
        command = self.Command()
        result = command.do_command()
        self.assertEqual(
            set(["update", "response"]), set(result.keys()),
        )
        self.assertIsNone(result["update"])

        update = "test"
        result = command.do_command(update)
        self.assertEqual(result["update"], update)
        self.assertEqual(result["response"], self.message)
