import unittest
from unittest.mock import patch

from .. import news

from bs4 import BeautifulSoup


class TestNews(unittest.TestCase):
    """Test news functionalities."""

    @patch("pugsebot.commands.news.get_html_soup")
    def test_function(self, get_html_soup):
        """Test news function."""
        result = BeautifulSoup(
            '<h3 class="event-title"><a href="http://url.com">Title</a></h3>',
            "html.parser",
        )
        get_html_soup.return_value = result
        result = news.News().function()
        self.assertIn("notícia", result)
        self.assertIn("http", result)
