import os
import unittest

from commands.help import Help


class TestHelp(unittest.TestCase):
    """Test help functionalities."""

    def test_function(self):
        """Test help function."""
        command_list = os.listdir("commands")
        command_list = [
            command.replace(".py", "")
            for command in command_list
            if command not in ["__init__.py", "__pycache__"]
        ]

        result = Help().function()
        for command in command_list:
            self.assertIn("/" + command, result)
