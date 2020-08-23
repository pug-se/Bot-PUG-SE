# raise NotImplementedError
import unittest

from utils import logging


class TestLoggers(unittest.TestCase):
    """Test logging functionalities."""

    def setUp(self):
        self.level = logging.logger_list[0].level

    def tearDown(self):
        logging.set_level(self.level)

    def test_default_level(self):
        """Default level must be info."""
        for logger in logging.logger_list:
            self.assertEqual(20, logger.level)

    def test_set_level(self):
        """Test set level function."""
        logging.set_level("DEBUG")
        for logger in logging.logger_list:
            self.assertEqual(10, logger.level)
