import unittest

import utils


class TestUtilsSchedule(unittest.TestCase):
    """Test utils.schedule functionality."""

    def test_Schedule(self):
        """Test Schedule initialization."""
        schedule = utils.schedule.Schedule("test", None, "send_photo", None)
        self.assertEqual(schedule.format, "photo")

        schedule = utils.schedule.Schedule("test", None, "send_text", None)
        self.assertEqual(schedule.format, "text")

        schedule = utils.schedule.Schedule("test", None, "reply_text", None)
        self.assertEqual(schedule.format, "text")

        schedule = utils.schedule.Schedule("test", None, "reply_photo", None)
        self.assertEqual(schedule.format, "photo")

        schedule = utils.schedule.Schedule("test", None, "teste", None)
        self.assertEqual(schedule.format, "text")
