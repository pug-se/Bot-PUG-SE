import unittest
from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

from commands import udemy

"""'

"""


class TestUdemy(unittest.TestCase):
    """Test udemy functionalities."""

    @patch("commands.udemy.get_html_soup")
    def test_function(self, get_html_soup):
        """Test udemy function."""
        get_html_soup.return_value = BeautifulSoup(
            '<h3><a href="http://url.com">Test</a></h3>', "html.parser"
        )
        result = udemy.Udemy().function()
        self.assertIn("Udemy", result)
        self.assertIn("http", result)
