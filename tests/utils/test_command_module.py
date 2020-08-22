import unittest

import utils
import commands


class TestUtilsCommandModule(unittest.TestCase):
    """Test command_module functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the commands path and module name."""
        cls.commands_path = utils.command_modules.get_commands_path()
        cls.commands_module_name = "commands"

    def assert_get_commands(self, command_list):
        """Assert about get_commands functionality."""
        Base = utils.command_base.CommandBase
        for command in command_list:
            self.assertNotEqual(type(command), Base)
            self.assertTrue(isinstance(command, Base))

    def test_get_commands(self):
        """Test get_commands."""
        command_list = utils.command_modules.get_commands()
        self.assert_get_commands(command_list)

    def test_get_commands_by_modules(self):
        """Test get_commands_by_modules."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        modules = utils.command_modules.get_modules_by_names(
            names, self.commands_module_name,
        )
        command_list = utils.command_modules.get_commands_by_modules(modules)

        self.assert_get_commands(command_list)

    def assert_get_modules(self, modules):
        """Assert about get_modules."""
        attr_names = dir(commands)
        attr_list = [getattr(commands, attr_str) for attr_str in attr_names]

        for module in modules:
            self.assertIn(module, attr_list)

    def test_get_modules_by_path(self):
        """Test get_modules_by_path."""
        modules = utils.command_modules.get_modules_by_path(self.commands_path)

        self.assert_get_modules(modules)

    def test_get_modules_by_names(self):
        """Test get_module_by_names."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        modules = utils.command_modules.get_modules_by_names(
            names, self.commands_module_name,
        )

        self.assert_get_modules(modules)

    def test_get_module_names(self):
        """Test get_module_names."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        for name in names:
            self.assertTrue(hasattr(commands, name))

    def test_get_package_name(self):
        """Test get_package_name."""
        name = utils.command_modules.get_package_name(self.commands_path)
        self.assertEqual(name, self.commands_module_name)
