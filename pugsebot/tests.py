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

class TestUtilsInit(unittest.TestCase):
    def test_get_module_names(self):
        names = commands.get_module_names()
        for name in names:
            self.assertTrue(
                hasattr(commands, name)
            )

    def test_get_modules(self):
        names = commands.get_module_names()
        modules = commands.get_modules(names)

        attr_names = dir(commands)
        attr_list = [
            getattr(commands, attr_str) for attr_str in attr_names
        ]

        for module in modules:
            self.assertIn(module, attr_list)

    def test_get_commands(self):
        names = commands.get_module_names()
        modules = commands.get_modules(names)
        command_list = commands.get_commands(modules)

        Base = utils.command_base.CommandBase
        for command in command_list:
            self.assertNotEqual(
                type(command), Base)
            self.assertTrue(
                isinstance(command, Base))

class TestUtilsDatabaseCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Cache = utils.database.Cache

    def setUp(self):
        expire_time = \
            datetime.datetime.now()\
            + datetime.timedelta(seconds=3)
        self.expire_time = expire_time
        self.text = 'test text'
        self.key = 'test'
        try:
            # tenta deletar uma cache teste
            # resultante de execuções interrompidas
            cached_test = self.Cache.get(
                self.Cache.key == self.key)
            cached_test.delete_instance()
        except:
            pass
        self.Cache.create(
            key=self.key,
            result=self.text,
            expire_time=self.expire_time,
        )

    def tearDown(self):
        try:
            test = self.Cache.get(
                self.Cache.key == self.key)
            test.delete_instance()
        except:
            pass

    def test_get_value_valid(self):
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertEqual(test.expire_time, self.expire_time)

    def test_get_value_invalid_key(self):
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)

    def test_get_value_invalid_expire(self):
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        time.sleep(4)
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_set_value_new(self):
        test = self.Cache.get_value(self.key)
        test.delete_instance()
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)
        new_time = 3
        test = self.Cache.set_value(
            self.key, self.text, new_time)
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertNotEqual(test.expire_time, self.expire_time)

    def test_set_value_old(self):
        new_time = 4
        new_text = self.text + 'test'
        test = self.Cache.set_value(
            self.key, new_text, new_time)
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, new_text)
        self.assertNotEqual(
            test.expire_time, self.expire_time)

    def test_remove_value_exist(self):
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertTrue(
            self.Cache.remove_value(self.key))
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_remove_value_no_exist(self):
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)
        self.assertFalse(
            self.Cache.remove_value('test2'))
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)

class TestUtilsDatabaseCommandInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.CommandInfo = utils.database.CommandInfo

    def setUp(self):
        self.command_name = 'test'
        self.key = 'test'
        self.info = 'test'
        try:
            # tenta deletar uma cache teste
            # resultante de execuções interrompidas
            info_test = self.CommandInfo.get(
                (self.CommandInfo.command_name == self.command_name)
                & (self.CommandInfo.key == self.key)
            )
            info_test.delete_instance()
        except:
            pass
        self.CommandInfo.create(
            command_name=self.command_name,
            key=self.key,
            info=self.info,
        )

    def tearDown(self):
        try:
            info_test = self.CommandInfo.get(self.CommandInfo.key == self.key)
            info_test.delete_instance()
        except:
            pass

    def test_get_value_valid(self):
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, self.info)
        self.assertEqual(test.command_name, self.command_name)

    def test_get_value_invalid_key(self):
        test = self.CommandInfo.get_value(
            'test2', 'test2')
        self.assertIsNone(test)

    def test_set_value_new(self):
        test = self.CommandInfo.get_value(self.command_name, self.key)
        test.delete_instance()
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNone(test)

        new_info = 'test3'
        test = self.CommandInfo.set_value(
            self.command_name, self.key, new_info)
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.command_name, self.command_name)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, new_info)

    def test_set_value_old(self):
        new_info = 'test3'
        test = self.CommandInfo.set_value(
            self.command_name, self.key, new_info)
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.command_name, self.command_name)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, new_info)

    def test_remove_value_exist(self):
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertTrue(
            self.CommandInfo.remove_value(
                self.command_name, self.key))
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNone(test)

    def test_remove_value_no_exist(self):
        test = self.CommandInfo.get_value(
            self.command_name, 'teste2')
        self.assertIsNone(test)
        self.assertFalse(
            self.CommandInfo.remove_value(
                self.command_name, 'teste2'))

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

class TestUtilsCommandBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.message = 'test'
        cls.name = 'test'
        cls.help_text = 'test'
        cls.reply_function_name = 'reply_text'

        class MockCommand(utils.command_base.CommandBase):
            def __init__(self, interval=None, expire=None):
                super().__init__(
                    name=cls.name,
                    help_text=cls.help_text,
                    reply_function_name=cls.reply_function_name,
                    schedule_interval=interval,
                    expire=expire,
                )

            def function(self, update=None, context=None):
                return cls.message

        cls.Command = MockCommand

    def setUp(self):
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(
            self.name, self.message)

    def tearDown(self):
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(
            self.name, self.message)

    def test_set_info(self):
        command = self.Command()
        info = utils.database.CommandInfo.get_value(
            command_name=self.name, key=self.message
        )
        self.assertIsNone(info)

        text = 'test2'
        command.set_info(self.message, text)
        info = utils.database.CommandInfo.get_value(
            command_name=self.name, key=self.message
        )
        self.assertIsNotNone(info)
        self.assertEqual(info.key, self.message)
        self.assertEqual(info.info, text)

    def test_get_info(self):
        command = self.Command()

        info = command.get_info(self.message)
        self.assertIsNone(info)

        text = 'test2'
        command.set_info(self.message, text)
        info = command.get_info(self.message)
        self.assertIsNotNone(info)
        self.assertEqual(info, text)

    def test_remove_info(self):
        command = self.Command()
        removed = command.remove_info(self.message)
        self.assertFalse(removed)

        text = 'test2'
        command.set_info(self.message, text)

        removed = command.remove_info(self.message)
        self.assertTrue(removed)

    def test_get_result_cache(self):
        expire = 3
        command = self.Command(expire=expire)

        value = utils.database.Cache.get_value(self.name)
        self.assertIsNone(value)

        result = command.get_result()
        self.assertEqual(result, self.message)

        value = utils.database.Cache.get_value(self.name)
        self.assertIsNotNone(value)
        self.assertEqual(value.key, self.name)
        self.assertEqual(value.result, self.message)

    def test_get_result_no_cache(self):
        command = self.Command()
        result = command.get_result()
        self.assertEqual(result, self.message)

    def test_get_schedule(self):
        command = self.Command()
        schedule = command.get_schedule()
        self.assertIsNone(schedule)

        command_sched = self.Command(5)
        schedule = command_sched.get_schedule()
        self.assertTrue(
            isinstance(schedule, utils.schedule.Schedule))

    def test_function_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            utils.command_base.CommandBase(None, None, None, None).function()

    def test_function(self):
        self.assertEqual(self.Command().function(), self.message)

    def test_init(self):
        command = self.Command()
        self.assertEqual(command.name, self.name)
        self.assertEqual(command.help_text, self.help_text)
        self.assertEqual(
            command.reply_function_name,
            self.reply_function_name,
        )

        interval = 1
        expire = 1
        command = self.Command(interval, expire)
        self.assertEqual(
            command.interval, interval)
        self.assertEqual(
            command.expire, expire)

    def test_do_command(self):
        command = self.Command()
        result = command.do_command()
        self.assertEqual(
            set(['update', 'response']),
            set(result.keys()),
        )
        self.assertIsNone(result['update'])

        update = 'test'
        result = command.do_command(update)
        self.assertEqual(result['update'], update)
        self.assertEqual(result['response'], self.message)

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

class TestFAQ(unittest.TestCase):
    def test_function(self):
        result = commands.faq.FAQ().function()
        self.assertIn('O que é Python?', result)
        self.assertIn('https://www.python.org/dev/peps/pep-0008', result)

if __name__ == '__main__':
    unittest.main()
