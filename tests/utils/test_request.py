import unittest
import json

import utils


class TestUtilsRequest(unittest.TestCase):
    """Test Request functionalities."""

    def test_get_html_soup(self):
        """Test get_html_soup."""
        soup = utils.request.get_html_soup("https://google.com")
        self.assertIn("Google", soup.text)

        soup = utils.request.get_html_soup("test")
        self.assertIsNone(soup)

    def test_get_json(self):
        """Test get_json."""
        result = utils.request.get_json("test")
        self.assertIsInstance(result, dict)

    def test_telegram_send_photo(self):
        """Test telegram_send_photo."""
        text = "Estou sendo testado! Desculpe o incomodo..."

        response = utils.request.telegram_send_message(
            text, utils.environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict["ok"])
        self.assertEqual(
            str(result_dict["result"]["chat"]["id"]),
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertTrue(result_dict["result"]["from"]["is_bot"],)
        self.assertEqual(
            str(result_dict["result"]["text"]), text,
        )

    def test_telegram_send_message(self):
        """Test telegram_send_message."""
        text = (
            "http://www.ellasaude.com.br/blog/wp-content"
            "/uploads/2017/10/128-768x404.jpg"
        )

        response = utils.request.telegram_send_photo(
            text, utils.environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict["ok"])
        self.assertEqual(
            str(result_dict["result"]["chat"]["id"]),
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertTrue(result_dict["result"]["from"]["is_bot"],)
        self.assertIsNotNone(result_dict["result"]["photo"],)
