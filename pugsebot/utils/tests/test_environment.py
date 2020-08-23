import os

import unittest
from unittest.mock import Mock, patch

from .. import environment


class TestEnvironmentDatabase(unittest.TestCase):
    """Test about functionalities."""

    @patch("pugsebot.utils.environment.sys")
    def test_database_url_not_testing(self, sys):
        """Test get_database_url outside test session."""
        sys.modules = []

        get_db_url_result = environment.get_database_url()
        db_url_env = os.environ.get("DATABASE_URL", None)

        if db_url_env and db_url_env != environment.default_db_url:
            self.assertNotEqual(environment.default_db_url, get_db_url_result)
        else:
            self.assertEqual(environment.default_db_url, get_db_url_result)

    def test_database_url_testing(self):
        """Test get_database_url inside test session."""
        get_db_url_result = environment.get_database_url()
        self.assertEqual(environment.default_db_url, get_db_url_result)
