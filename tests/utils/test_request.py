import unittest
from unittest.mock import Mock, patch
import json

from utils import request
from utils import environment


class TestRequest(unittest.TestCase):
    """Test Request functionalities."""

    @patch("utils.request.requests.get")
    def test_get_html_soup_success(self, get):
        """Test get_html_soup success."""
        mock_response = Mock(spec=request.requests.models.Response())
        mock_response.text = "<body>Google</body>"
        get.return_value = mock_response

        soup = request.get_html_soup("https://google.com")
        self.assertIn("Google", soup.text)

    @patch("utils.request.requests")
    def test_get_html_soup_fail(self, requests):
        """Test get_html_soup fail."""

        def raise_ex(*args, **kwargs):
            raise Exception

        requests.get = raise_ex
        soup = request.get_html_soup("test")
        self.assertIsNone(soup)

    @patch("utils.request.requests.get")
    def test_get_json(self, get):
        """Test get_json."""
        get.return_value = "{}"

        result = request.get_json("test")
        self.assertIsInstance(result, dict)

    @patch("utils.request.requests.post")
    def test_telegram_send_photo(self, post):
        """Test telegram_send_photo."""
        text = "Test"
        response = Mock()
        response.text = f"""{{
            "ok":true,
            "result":{{
                "message_id":"",
                "from":{{
                    "id":0,
                    "is_bot":true,
                    "first_name":"",
                    "username":""
                }},
                "chat":{{
                    "id":{environment.TARGET_CHAT_ID},
                    "first_name":"",
                    "last_name":"",
                    "username":"",
                    "type":""
                }},
                "date":"",
                "text":"{text}"
            }} 
        }}"""

        response.status_code = 200
        post.return_value = response

        response = request.telegram_send_message(
            text, environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict["ok"])
        self.assertEqual(
            str(result_dict["result"]["chat"]["id"]),
            environment.TARGET_CHAT_ID,
        )
        self.assertTrue(result_dict["result"]["from"]["is_bot"],)
        self.assertEqual(
            str(result_dict["result"]["text"]), text,
        )

    @patch("utils.request.requests.post")
    def test_telegram_send_message(self, post):
        """Test telegram_send_message."""

        text = (
            "http://www.ellasaude.com.br/blog/wp-content"
            "/uploads/2017/10/128-768x404.jpg"
        )
        response = Mock()
        response.text = f"""{{
            "ok":true,
            "result":{{
                "message_id":"",
                "from":{{
                    "id":0,
                    "is_bot":true,
                    "first_name":"",
                    "username":""
                }},
                "chat":{{
                    "id":{environment.TARGET_CHAT_ID},
                    "first_name":"",
                    "last_name":"",
                    "username":"",
                    "type":""
                }},
                "date":"",
                "photo":"{text}"
            }} 
        }}"""
        response.status_code = 200
        post.return_value = response

        response = request.telegram_send_photo(
            text, environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict["ok"])
        self.assertEqual(
            str(result_dict["result"]["chat"]["id"]),
            environment.TARGET_CHAT_ID,
        )
        self.assertTrue(result_dict["result"]["from"]["is_bot"],)
        self.assertIsNotNone(result_dict["result"]["photo"],)
