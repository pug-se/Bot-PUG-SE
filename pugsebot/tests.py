import unittest
from datetime import datetime
from unittest import mock
import threading

from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.message import Message

import bot 
import utils

def mock_update(message_text):
    message = Message(
        0, from_user=None, date=None,
        chat=0, text=message_text
    )
    return Update(0, message=message)

class TestPUGSEBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        threading
        cls.bot = bot.PUGSEBot()
        cls.bot.chat_id = None

    def test_say(self):
        update = mock_update(
            message_text='test'
        ) 
        update = self.bot.say(update)
        self.assertIn('test', update.message.text)

    def test_get_udemy_coupons(self):
        message = self.bot.get_udemy_coupons()
        self.assertIn('Udemy', message)

    def test_get_python_news(self):
        message = self.bot.get_python_news()
        self.assertIn('notícia', message)

    def test_get_about(self):
        message = self.bot.get_about()
        self.assertIn('PUG-SE', message)

    def test_get_memes(self):
        message = self.bot.get_memes() 
        self.assertIn('https:', message)
        self.assertIn('.png', message)

    def test_get_projects(self):
        message = self.bot.get_projects() 
        self.assertIn(
            'https://github.com/pug-se', 
            message,
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

class TestMemes(unittest.TestCase):
    def test_get_url_image_vida_programador(self):
        pass   
    
    def test_get_url_image_turnoff_us(self):
        pass   

    def test_get_random_meme_image(self):
        pass   

if __name__ == '__main__':
    unittest.main()