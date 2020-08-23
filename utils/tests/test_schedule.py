import unittest

from utils import schedule


class TestSchedule(unittest.TestCase):
    """Test schedule functionality."""

    def test_Schedule_methods(self):
        """Test Schedule initialization."""
        sched = schedule.Schedule("test", None, "send_photo", None)
        self.assertEqual(sched.format, "photo")

        sched = schedule.Schedule("test", None, "send_text", None)
        self.assertEqual(sched.format, "text")

        sched = schedule.Schedule("test", None, "reply_text", None)
        self.assertEqual(sched.format, "text")

        sched = schedule.Schedule("test", None, "reply_photo", None)
        self.assertEqual(sched.format, "photo")

    def test_schedule_invalid_method(self):
        """Schedule must return default method, text."""
        sched = schedule.Schedule("test", None, "teste", None)
        self.assertEqual(sched.format, "text")
