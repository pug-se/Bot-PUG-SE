import unittest
from unittest.mock import patch

from commands import book


class TestBook(unittest.TestCase):
    """Test book functionalities."""

    @patch("commands.book.get_json")
    def test_function(self, get_json):
        """Test book function."""
        get_json.return_value = {
            "data": [{"productId": ""}],
            "title": "",
            "oneLiner": "",
        }
        result = book.Book().function()
        self.assertIn("Livro", result)
        self.assertIn("gratuito", result)
        self.assertIn("https://www.packtpub.com/free-learning", result)
