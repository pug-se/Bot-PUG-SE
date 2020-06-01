import unittest
from datetime import datetime
from unittest import mock
import threading

from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.message import Message

import bot
import utils
from functions import say, news, udemy, memes, about, projects

def mock_update(message_text):
    message = Message(
        0, from_user=None, date=None,
        chat=0, text=message_text
    )
    return Update(0, message=message)

def mock_reply_method(update=None, content=None):
    return mock_update(content)

class TestPUGSEBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        threading
        cls.bot = bot.PUGSEBot()        
        cls.bot.chat_id = None

    def test_say(self):
        reply = say.reply(mock_reply_method)
        update = reply(mock_update('/say test'))
        self.assertIn('test', update.message.text)

    def test_get_udemy_coupons(self):
        reply = udemy.reply(mock_reply_method)
        update = reply()
        self.assertIn('Udemy', update.message.text)

    def test_get_python_news(self):
        reply = news.reply(mock_reply_method)
        update = reply()
        self.assertIn('notícia', update.message.text)

    def test_get_about(self):
        reply = about.reply(mock_reply_method)
        update = reply()
        self.assertIn('PUG-SE', update.message.text)

    def test_get_memes(self):
        reply = memes.reply(mock_reply_method)
        update = reply()
        self.assertIn('https:', update.message.text)
        self.assertIn('.png', update.message.text)

    def test_get_projects(self):
        reply = projects.reply(mock_reply_method)
        update = reply()
        self.assertIn(
            'https://github.com/pug-se', 
            update.message.text,
        )

    def test_add_schedules(self):
        self.bot.add_schedules()
        self.assertNotEqual(
            self.bot.schedule_manager.schedules, 
            {},
        )

class TestUtils(unittest.TestCase):
    def test_get_html_soup(self):
        soup = utils.get_html_soup('https://google.com')
        self.assertIn('Google', soup.text)

        soup = utils.get_html_soup('test')
        self.assertIsNone(soup)

    def test_get_json(self):
        result = utils.get_json('test')
        self.assertIsInstance(result, dict)

class TestMemes(unittest.TestCase):
    def test_get_url_image_vida_programador(self):
        pass   
    
    def test_get_url_image_turnoff_us(self):
        pass   

    def test_get_random_meme_image(self):
        pass   

if __name__ == '__main__':
    unittest.main()
