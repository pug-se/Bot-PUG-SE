import unittest
from unittest.mock import patch

from .. import projects


class TestProjects(unittest.TestCase):
    """Test projects functionalities."""

    @patch("pugsebot.commands.projects.get_json")
    def test_function(self, get_json):
        """Test projects function."""
        get_json.return_value = [
            {"name": "", "description": "", "html_url": "http://url.com"}
        ]

        result = projects.Projects().function()
        self.assertIn("projetos", result)
        self.assertIn("http", result)
