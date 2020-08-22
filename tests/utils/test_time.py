import unittest

from utils import time


class TestUtilsTime(unittest.TestCase):
    """Test Request functionalities."""

    def test_UM_DIA_EM_SEGUNDOS(self):
        """Test total seconds at UM_DIA_EM_SEGUNDOS."""
        self.assertEqual(
            time.UM_DIA_EM_SEGUNDOS, 60 * 60 * 24,
        )

    def test_UMA_HORA_EM_SEGUNDOS(self):
        """Test total seconds at UMA_HORA_EM_SEGUNDOS."""
        self.assertEqual(
            time.UMA_HORA_EM_SEGUNDOS, 60 * 60,
        )

    def test_UMA_SEMANA_EM_SEGUNDOS(self):
        """Test total seconds at UMA_SEMANA_EM_SEGUNDOS."""
        self.assertEqual(
            time.UMA_SEMANA_EM_SEGUNDOS, 60 * 60 * 24 * 7,
        )
