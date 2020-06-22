import unittest
import json
import time
import datetime

from telegram.update import Update
from telegram.message import Message

import bot
import utils
import commands

utils.logging.set_level('ERROR')

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
        cls.bot = bot.PUGSEBot(utils.environment.TOKEN)
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

class TestUtilsCache(unittest.TestCase):
    def setUp(self):
        expire_time = \
            datetime.datetime.now()\
            + datetime.timedelta(seconds=3)
        self.expire_time = expire_time
        self.text = 'test text'
        self.key = 'test'
        utils.cache.Cache.create(
            key=self.key,
            result=self.text,
            expire_time=self.expire_time,
        )

    def tearDown(self):
        try:
            test = utils.cache.Cache.get(
            utils.cache.Cache.key == self.key)
            test.delete_instance()
        except:
            pass

    def test_get_value_valid(self):
        test = utils.cache.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertEqual(test.expire_time, self.expire_time)

    def test_get_value_invalid_key(self):
        test = utils.cache.Cache.get_value('test2')
        self.assertIsNone(test)

    def test_get_value_invalid_expire(self):
        test = utils.cache.Cache.get_value('test')
        self.assertIsNotNone(test)
        time.sleep(4)
        test = utils.cache.Cache.get_value('test')
        self.assertIsNone(test)


    def test_set_value_new(self):
        test = utils.cache.Cache.get(
        utils.cache.Cache.key == self.key)
        test.delete_instance()
        test = utils.cache.Cache.get_value('test')
        self.assertIsNone(test)
        new_time = 3
        test = utils.cache.Cache.set_value(
            self.key, self.text, new_time)
        test = utils.cache.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertNotEqual(test.expire_time, self.expire_time)

    def test_set_value_old(self):
        new_time = 4
        new_text = self.text + 'test'
        test = utils.cache.Cache.set_value(
            self.key, new_text, new_time)
        test = utils.cache.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, new_text)
        self.assertNotEqual(
            test.expire_time, self.expire_time)

class TestUtilsTime(unittest.TestCase):
    def test_UM_DIA_EM_SEGUNDOS(self):
        self.assertEqual(
            utils.time.UM_DIA_EM_SEGUNDOS, 60 * 60 * 24,
        )

    def test_UMA_HORA_EM_SEGUNDOS(self):
        self.assertEqual(
            utils.time.UMA_HORA_EM_SEGUNDOS, 60 * 60,
        )

    def test_UMA_SEMANA_EM_SEGUNDOS(self):
        self.assertEqual(
            utils.time.UMA_SEMANA_EM_SEGUNDOS, 60 * 60 * 24 * 7,
        )

class TestUtilsRequest(unittest.TestCase):
    def test_get_html_soup(self):
        soup = utils.request.get_html_soup('https://google.com')
        self.assertIn('Google', soup.text)

        soup = utils.request.get_html_soup('test')
        self.assertIsNone(soup)

    def test_get_json(self):
        result = utils.request.get_json('test')
        self.assertIsInstance(result, dict)

    def test_telegram_send_photo(self):
        text = 'Estou sendo testado! Desculpe o incomodo...'

        response = utils.request.telegram_send_message(
            text,
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict['ok'])
        self.assertEqual(
            str(result_dict['result']['chat']['id']),
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertTrue(
            result_dict['result']['from']['is_bot'],
        )
        self.assertEqual(
            str(result_dict['result']['text']),
            text,
        )

    def test_telegram_send_message(self):
        text = 'http://www.ellasaude.com.br/blog/wp-content'\
            '/uploads/2017/10/128-768x404.jpg'

        response = utils.request.telegram_send_photo(
            text,
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertEqual(response.status_code, 200)

        result_dict = json.loads(response.text)
        self.assertTrue(result_dict['ok'])
        self.assertEqual(
            str(result_dict['result']['chat']['id']),
            utils.environment.TARGET_CHAT_ID,
        )
        self.assertTrue(
            result_dict['result']['from']['is_bot'],
        )
        self.assertIsNotNone(
            result_dict['result']['photo'],
        )

class TestUtilsCommand(unittest.TestCase):
    def test_Command(self):
        with self.assertRaises(NotImplementedError):
            utils.command_base.CommandBase(None, None, None, None).function()

        class MockCommand(utils.command_base.CommandBase):
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

class TestUtilsSchedule(unittest.TestCase):
    def test_Schedule(self):
        schedule = utils.schedule.Schedule('test', None, 'send_photo', None)
        self.assertEqual(schedule.format, 'photo')

        schedule = utils.schedule.Schedule('test', None, 'send_text', None)
        self.assertEqual(schedule.format, 'text')

        schedule = utils.schedule.Schedule('test', None, 'reply_text', None)
        self.assertEqual(schedule.format, 'text')

        schedule = utils.schedule.Schedule('test', None, 'reply_photo', None)
        self.assertEqual(schedule.format, 'photo')

        schedule = utils.schedule.Schedule('test', None, 'teste', None)
        self.assertEqual(schedule.format, 'text')

class TestAbout(unittest.TestCase):
    def test_function(self):
        result = commands.about.About().function()
        self.assertIn('comunidade', result)
        self.assertIn('contribuir', result)

class TestLinks(unittest.TestCase):
    def test_function(self):
        result = commands.links.Links().function()
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
        result = commands.news.News().function()
        self.assertIn('notícia', result)
        self.assertIn('http', result)

class TestProjects(unittest.TestCase):
    def test_function(self):
        result = commands.projects.Projects().function()
        self.assertIn('projetos', result)
        self.assertIn('http', result)

class TestSay(unittest.TestCase):
    def test_function(self):
        result = commands.say.Say().function()
        self.assertEqual('', result)

        result = commands.say.Say().function(mock_update('test'))
        self.assertEqual('test', result)

class TestUdemy(unittest.TestCase):
    def test_function(self):
        result = commands.udemy.Udemy().function()
        self.assertIn('Udemy', result)
        self.assertIn('http', result)

if __name__ == '__main__':
    unittest.main()
