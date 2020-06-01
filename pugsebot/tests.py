import unittest
from datetime import datetime
from unittest import mock
import os

from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.message import Message
from telegram.ext import Updater

import bot
import utils
import commands

token = os.environ['TELEGRAM_KEY_TEST']

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
        cls.bot = bot.PUGSEBot(token)        
        cls.bot.chat_id = None

    def test_add_commands(self):
        handler_list = self.bot.dp.handlers[0]
        self.assertEqual(
            len(handler_list) - 1, 
            len(commands.command_list),
        )
        name_list1 = [
            command.name for command in commands.command_list
        ]
        name_list2 = []
        for handler in handler_list:
            name_list2.append(handler.command[0])
        self.assertEqual(
            set(name_list1).symmetric_difference(set(name_list2)),
             set(['help']),
        )

    def test_help(self):
        handler_list = self.bot.dp.handlers[0]
        name_list = [
            handler.command[0] for handler in handler_list
        ]
        self.assertIn('help',name_list)
 
class TestUtils(unittest.TestCase):
    def test_get_html_soup(self):
        soup = utils.get_html_soup('https://google.com')
        self.assertIn('Google', soup.text)

        soup = utils.get_html_soup('test')
        self.assertIsNone(soup)

    def test_get_json(self):
        result = utils.get_json('test')
        self.assertIsInstance(result, dict)

    def test_Command_function(self):
        with self.assertRaises(TypeError):
            utils.Command(None, None, None).function()

class TestAbout(unittest.TestCase):
    def test_function(self):
        pass

class TestMemes(unittest.TestCase):
    def test_get_url_image_vida_programador(self):
        pass   
    
    def test_get_url_image_turnoff_us(self):
        pass   

    def test_get_random_meme_image(self):
        pass  

class TestNews(unittest.TestCase):
    def test_function(self):
        result = commands.News().function()
        self.assertEqual(
            set(['update','text']), 
            set(result.keys()),
        )
        self.assertIsNone(result['update'])
        self.assertIn('notícia', result['text'])

class TestProjects(unittest.TestCase):
    def test_function(self):
        result = commands.Projects().function()
        self.assertEqual(
            set(['update','text']), 
            set(result.keys()),
        )
        self.assertIsNone(result['update'])
        self.assertIn('projetos', result['text'])

class TestSay(unittest.TestCase):
    def test_function(self):
        result = commands.Say().function()
        self.assertEqual(
            set(['text']), 
            set(result.keys()),
        )
        self.assertEqual('', result['text'])

        result = commands.Say().function(mock_update('test'))
        self.assertEqual(
            set(['text']), 
            set(result.keys()),
        )
        self.assertEqual('test', result['text'])

class TestUdemy(unittest.TestCase):
    def test_function(self):
        result = commands.Udemy().function()
        self.assertEqual(
            set(['update','text']), 
            set(result.keys()),
        )
        self.assertIsNone(result['update'])
        self.assertIn('Udemy', result['text'])
        self.assertIn('https://', result['text'])

if __name__ == '__main__':
    unittest.main()

