import unittest

from commands.about import About


class TestAbout(unittest.TestCase):
    """Test about functionalities."""

    def test_function(self):
        """Test about function."""
        result = About().function()
        self.assertIn("comunidade", result)
        self.assertIn("contribuir", result)
