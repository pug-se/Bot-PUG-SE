import unittest
from unittest.mock import Mock, patch

from .. import database, schedule, command
from ... import commands


class TestCommandFinder(unittest.TestCase):
    """Test command_module functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the commands path and module name."""
        cls.commands_path = command.get_commands_path()
        cls.commands_module_name = "pugsebot.commands"

    def assert_get_commands(self, command_list):
        """Assert about get_commands functionality."""
        Base = command.CommandBase
        for comm in command_list:
            self.assertNotEqual(type(comm), Base)
            self.assertTrue(isinstance(comm, Base))

    def test_get_commands(self):
        """Test get_commands."""
        command_list = command.get_commands()
        self.assert_get_commands(command_list)

    def test_get_commands_by_modules(self):
        """Test get_commands_by_modules."""
        names = command.get_modules_names(self.commands_path)
        modules = command.get_modules_by_names(
            names, self.commands_module_name,
        )
        command_list = command.get_commands_by_modules(modules)

        self.assert_get_commands(command_list)

    def assert_get_modules(self, modules):
        """Assert about get_modules."""
        attr_names = dir(commands)
        attr_list = [getattr(commands, attr_str) for attr_str in attr_names]

        for module in modules:
            self.assertIn(module, attr_list)

    def test_get_modules_by_path(self):
        """Test get_modules_by_path."""
        modules = command.get_modules_by_path(self.commands_path)
        self.assert_get_modules(modules)

    def test_get_modules_by_names(self):
        """Test get_module_by_names."""
        names = command.get_modules_names(self.commands_path)
        modules = command.get_modules_by_names(
            names, self.commands_module_name,
        )

        self.assert_get_modules(modules)

    def test_get_module_names(self):
        """Test get_module_names."""
        names = command.get_modules_names(self.commands_path)
        for name in names:
            self.assertTrue(hasattr(commands, name))

    def test_get_package_name(self):
        """Test get_package_name."""
        name = command.get_package_name(self.commands_path)
        self.assertEqual(name, self.commands_module_name)


class TestCommandBase(unittest.TestCase):
    """Test CommandBase functionalities."""

    @classmethod
    def setUpClass(cls):
        """Mock a command."""
        cls.message = "test"
        cls.name = "test"
        cls.help_text = "test"
        cls.reply_function_name = "reply_text"

        class MockCommand(command.CommandBase):
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

    @patch("pugsebot.utils.command.CommandInfo")
    def test_set_info(self, CommandInfo):
        """Test set_info."""
        text = "test"
        command = self.Command()
        command.set_info(self.message, text)
        CommandInfo.set_value.assert_called_with(self.name, self.message, text)

    @patch("pugsebot.utils.command.CommandInfo.get_value")
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

    @patch("pugsebot.utils.command.CommandInfo.remove_value")
    def test_remove_info(self, remove_value):
        """Test remove_info."""
        command = self.Command()
        removed = command.remove_info(self.message)
        remove_value.assert_called_with(self.name, self.message)

    @patch("pugsebot.utils.command.Cache")
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
            command.CommandBase(None, None, None, None).function()

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
