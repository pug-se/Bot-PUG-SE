import unittest
from unittest.mock import Mock

from telegram.update import Update

from commands.say import Say


class TestSay(unittest.TestCase):
    """Test say functionalities."""

    def test_function(self):
        """Test say function."""
        result = Say().function()
        self.assertEqual("", result)

        message = "test"
        update = Mock(spec=Update("0"))
        update.message.text = "/say " + message

        result = Say().function(update)
        self.assertIn(message, result)
        self.assertNotIn("/say", result)
