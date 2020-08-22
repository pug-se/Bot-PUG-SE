import unittest

from commands.links import Links


class TestLinks(unittest.TestCase):
    """Test links functionalities."""

    def test_function(self):
        """Test links function."""
        result = Links().function()
        self.assertIn("links", result)
        self.assertIn("Python", result)
