import unittest

from commands.faq import FAQ


class TestFAQ(unittest.TestCase):
    """Test FAQ functionalities."""

    def test_function(self):
        """Test FAQ function."""
        result = FAQ().function()
        self.assertIn("O que é Python?", result)
        self.assertIn("https://www.python.org/dev/peps/pep-0008", result)
