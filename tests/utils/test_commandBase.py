import unittest

import utils


class TestUtilsCommandBase(unittest.TestCase):
    """Test CommandBase functionalities."""

    @classmethod
    def setUpClass(cls):
        """Mock a command."""
        cls.message = "test"
        cls.name = "test"
        cls.help_text = "test"
        cls.reply_function_name = "reply_text"

        class MockCommand(utils.command_base.CommandBase):
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

    def setUp(self):
        """Remove mocked values inside Cache and CommandInfo."""
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(self.name, self.message)

    def tearDown(self):
        """Remove mocked values inside Cache and CommandInfo."""
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(self.name, self.message)

    def test_set_info(self):
        """Test set_info."""
        command = self.Command()
        info = utils.database.CommandInfo.get_value(
            command_name=self.name, key=self.message
        )
        self.assertIsNone(info)

        text = "test2"
        command.set_info(self.message, text)
        info = utils.database.CommandInfo.get_value(
            command_name=self.name, key=self.message
        )
        self.assertIsNotNone(info)
        self.assertEqual(info.key, self.message)
        self.assertEqual(info.info, text)

    def test_get_info(self):
        """Test get_info."""
        command = self.Command()

        info = command.get_info(self.message)
        self.assertIsNone(info)

        text = "test2"
        command.set_info(self.message, text)
        info = command.get_info(self.message)
        self.assertIsNotNone(info)
        self.assertEqual(info, text)

    def test_remove_info(self):
        """Test remove_info."""
        command = self.Command()
        removed = command.remove_info(self.message)
        self.assertFalse(removed)

        text = "test2"
        command.set_info(self.message, text)

        removed = command.remove_info(self.message)
        self.assertTrue(removed)

    def test_get_result_cache(self):
        """Test get_result with cached results."""
        expire = 3
        command = self.Command(expire=expire)

        value = utils.database.Cache.get_value(self.name)
        self.assertIsNone(value)

        result = command.get_result()
        self.assertEqual(result, self.message)

        value = utils.database.Cache.get_value(self.name)
        self.assertIsNotNone(value)
        self.assertEqual(value.key, self.name)
        self.assertEqual(value.result, self.message)

    def test_get_result_no_cache(self):
        """Test get_result without cached results."""
        command = self.Command()
        result = command.get_result()
        self.assertEqual(result, self.message)

    def test_get_schedule(self):
        """Test get_schedule."""
        command = self.Command()
        schedule = command.get_schedule()
        self.assertIsNone(schedule)

        command_sched = self.Command(5)
        schedule = command_sched.get_schedule()
        self.assertTrue(isinstance(schedule, utils.schedule.Schedule))

    def test_function_not_implemented(self):
        """Test CommandBase function."""
        with self.assertRaises(NotImplementedError):
            utils.command_base.CommandBase(None, None, None, None).function()

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
