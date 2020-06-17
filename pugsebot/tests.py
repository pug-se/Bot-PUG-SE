import unittest
import json
import random
import time

from telegram.update import Update
from telegram.message import Message

import bot
import utils
import commands
import do_schedules

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
        cls.bot = bot.PUGSEBot(bot.token)
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
        self.assertIn('help', name_list)

class TestUtils(unittest.TestCase):
    def test_UM_DIA_EM_SEGUNDOS(self):
        self.assertEqual(
            utils.UM_DIA_EM_SEGUNDOS, 60 * 60 * 24,
        )

    def test_UMA_HORA_EM_SEGUNDOS(self):
        self.assertEqual(
            utils.UMA_HORA_EM_SEGUNDOS, 60 * 60,
        )

    def test_get_html_soup(self):
        soup = utils.get_html_soup('https://google.com')
        self.assertIn('Google', soup.text)

        soup = utils.get_html_soup('test')
        self.assertIsNone(soup)

    def test_get_json(self):
        result = utils.get_json('test')
        self.assertIsInstance(result, dict)

    def test_Command(self):
        with self.assertRaises(NotImplementedError):
            utils.Command(None, None, None, None).function()

        class MockCommand(utils.Command):
            def __init__(self):
                super().__init__(
                    name='test',
                    help_text='test',
                    reply_function_name='reply_text',
                    schedule_interval=None,
                )
            def function(self, update=None, context=None):
                return 'test'
        command = MockCommand()
        result = command.do_command()
        self.assertEqual(
            set(['update', 'response']),
            set(result.keys()),
        )
        self.assertIsNone(result['update'])
        result = command.do_command('test')
        self.assertEqual(result['update'], 'test')
        self.assertEqual(command.function(), 'test')
        self.assertEqual(result['response'], 'test')
        self.assertEqual(command.name, 'test')
        self.assertEqual(command.help_text, 'test')
        self.assertEqual(
            command.reply_function_name,
            'reply_text',
        )

    def test_Schedule(self):
        schedule = utils.Schedule(None, 'send_photo', None)
        self.assertEqual(schedule.format, 'photo')

        schedule = utils.Schedule(None, 'send_text', None)
        self.assertEqual(schedule.format, 'text')

        schedule = utils.Schedule(None, 'reply_text', None)
        self.assertEqual(schedule.format, 'text')

        schedule = utils.Schedule(None, 'reply_photo', None)
        self.assertEqual(schedule.format, 'photo')

        schedule = utils.Schedule(None, 'teste', None)
        self.assertEqual(schedule.format, 'text')

class TestDoSchedules(unittest.TestCase):
    def test_get_schedule_list(self):
        class MockCommand(utils.Command):
            def __init__(self):
                super().__init__(
                    name='test',
                    help_text='test',
                    reply_function_name='reply_text',
                    schedule_interval=1,
                )
            def function(self, update=None, context=None):
                return 'test'
        commands.command_list.append(MockCommand())

        schedule_list = do_schedules.get_schedule_list()
        self.assertEqual(
            schedule_list[-1].function(), 'test',
        )

    def test_send_message(self):
        text = 'Estou sendo testado! Desculpe o incomodo...'
        schedule = utils.Schedule(
            lambda update=None, context=None: text, 'text', 1,
        )
        response = do_schedules.send_message(
            schedule.function(),
            bot.target_chat_id,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict['ok'])
        self.assertEqual(
            str(result_dict['result']['chat']['id']),
            bot.target_chat_id,
        )
        self.assertTrue(
            result_dict['result']['from']['is_bot'],
        )
        self.assertEqual(
            str(result_dict['result']['text']),
            text,
        )

    def test_send_photo(self):
        text = 'http://www.ellasaude.com.br/blog/wp-content'\
            '/uploads/2017/10/128-768x404.jpg'
        schedule = utils.Schedule(
            lambda update=None, context=None: text, 'photo', 1,
        )
        response = do_schedules.send_photo(
            schedule.function(),
            bot.target_chat_id,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict['ok'])
        self.assertEqual(
            str(result_dict['result']['chat']['id']),
            bot.target_chat_id,
        )
        self.assertTrue(
            result_dict['result']['from']['is_bot'],
        )
        self.assertIsNotNone(
            result_dict['result']['photo'],
        )

class TestAbout(unittest.TestCase):
    def test_function(self):
        result = commands.About().function()
        self.assertIn('comunidade', result)
        self.assertIn('contribuir', result)

class TestLinks(unittest.TestCase):
    def test_function(self):
        result = commands.Links().function()
        self.assertIn('links', result)
        self.assertIn('Python', result)

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
        self.assertIn('notícia', result)
        self.assertIn('http', result)

class TestProjects(unittest.TestCase):
    def test_function(self):
        result = commands.Projects().function()
        self.assertIn('projetos', result)
        self.assertIn('http', result)

class TestSay(unittest.TestCase):
    def test_function(self):
        result = commands.Say().function()
        self.assertEqual('', result)

        result = commands.Say().function(mock_update('test'))
        self.assertEqual('test', result)

class TestUdemy(unittest.TestCase):
    def test_function(self):
        result = commands.Udemy().function()
        self.assertIn('Udemy', result)
        self.assertIn('http', result)

class TestCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache = utils.Cache('test', 1)

    @classmethod
    def tearDownClass(cls):
        cls.cache.clear()

    def test_no_defined(self):
        key = 'test_no_defined'
        self.assertIsNone(self.cache.get(key))

    def test_store(self):
        key = 'test_store'
        value = str(random.random())
        self.cache.set(key, value)
        self.assertEqual(value, self.cache.get(key))
        self.assertEqual(value, self.cache.get(key))

    def test_expire(self):
        key = 'test_expire'
        value = str(random.random())
        self.cache.set(key, value)
        self.assertEqual(value, self.cache.get(key))
        time.sleep(2)
        self.assertIsNone(self.cache.get(key))

if __name__ == '__main__':
    unittest.main()
