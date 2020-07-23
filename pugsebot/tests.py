"""Test bot functionalities."""

import unittest
import json
import time
import datetime

from telegram.update import Update
from telegram.message import Message

import bot
import utils
import commands
import commands.about
import commands.faq
import commands.links
import commands.memes
import commands.news
import commands.projects
import commands.say
import commands.udemy
import commands.help
import commands.packt

utils.logging.set_level('ERROR')

def mock_update(message_text):
    """Mock a python-telegram-bot update object."""
    message = Message(
        0, from_user=None, date=None,
        chat=0, text=message_text
    )
    return Update(0, message=message)

def mock_reply_method(update=None, content=None):
    """Mock a reply method."""
    return mock_update(content)

class TestPUGSEBot(unittest.TestCase):
    """Test bot functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the bot and chat id."""
        cls.bot = bot.PUGSEBot(utils.environment.TOKEN)
        cls.bot.chat_id = None

    def test_add_commands(self):
        """Test add_commands."""
        handler_list = self.bot.dp.handlers[0]
        command_list = utils.command_modules.get_commands()
        self.assertEqual(len(handler_list), len(command_list))
        name_list1 = [command.name for command in command_list]
        name_list2 = []
        for handler in handler_list:
            name_list2.append(handler.command[0])
        self.assertEqual(set(name_list1), set(name_list2))

class TestUtilsCommandModule(unittest.TestCase):
    """Test command_module functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the commands path and module name."""
        cls.commands_path = utils.command_modules.get_commands_path()
        cls.commands_module_name = 'commands'

    def assert_get_commands(self, command_list):
        """Assert about get_commands functionality."""
        Base = utils.command_base.CommandBase
        for command in command_list:
            self.assertNotEqual(type(command), Base)
            self.assertTrue(isinstance(command, Base))

    def test_get_commands(self):
        """Test get_commands."""
        command_list = utils.command_modules.get_commands()
        self.assert_get_commands(command_list)

    def test_get_commands_by_modules(self):
        """Test get_commands_by_modules."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        modules = utils.command_modules.get_modules_by_names(
            names,
            self.commands_module_name,
        )
        command_list = utils.command_modules.get_commands_by_modules(modules)

        self.assert_get_commands(command_list)

    def assert_get_modules(self, modules):
        """Assert about get_modules."""
        attr_names = dir(commands)
        attr_list = [
            getattr(commands, attr_str) for attr_str in attr_names
        ]

        for module in modules:
            self.assertIn(module, attr_list)

    def test_get_modules_by_path(self):
        """Test get_modules_by_path."""
        modules = utils.command_modules.get_modules_by_path(self.commands_path)

        self.assert_get_modules(modules)

    def test_get_modules_by_names(self):
        """Test get_module_by_names."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        modules = utils.command_modules.get_modules_by_names(
            names,
            self.commands_module_name,
        )

        self.assert_get_modules(modules)

    def test_get_module_names(self):
        """Test get_module_names."""
        names = utils.command_modules.get_modules_names(self.commands_path)
        for name in names:
            self.assertTrue(
                hasattr(commands, name)
            )

    def test_get_package_name(self):
        """Test get_package_name."""
        name = utils.command_modules.get_package_name(self.commands_path)
        self.assertEqual(name, self.commands_module_name)

class TestUtilsDatabaseCache(unittest.TestCase):
    """Test Cache functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the Cache object."""
        cls.Cache = utils.database.Cache

    def setUp(self):
        """Cache mock information."""
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
        """Delete cached information."""
        try:
            test = self.Cache.get(
                self.Cache.key == self.key)
            test.delete_instance()
        except:
            pass

    def test_get_value_valid(self):
        """Test get_value when value doesn't exist."""
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertEqual(test.expire_time, self.expire_time)

    def test_get_value_invalid_key(self):
        """Test get_value when value doesn't exist."""
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)

    def test_get_value_invalid_expire(self):
        """Test get_value when value is expired."""
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        time.sleep(4)
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_set_value_new(self):
        """Test set_value when value doesn't exist."""
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
        """Test set_value when value exists."""
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
        """Test remove_value when value exists."""
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertTrue(
            self.Cache.remove_value(self.key))
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_remove_value_no_exist(self):
        """Test remove_value when value doesn't exist."""
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)
        self.assertFalse(
            self.Cache.remove_value('test2'))
        test = self.Cache.get_value('test2')
        self.assertIsNone(test)

class TestUtilsDatabaseCommandInfo(unittest.TestCase):
    """Test CommandInfo functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the CommandInfo object."""
        cls.CommandInfo = utils.database.CommandInfo

    def setUp(self):
        """Store mock info."""
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
        """Delete mock info."""
        try:
            info_test = self.CommandInfo.get(self.CommandInfo.key == self.key)
            info_test.delete_instance()
        except:
            pass

    def test_get_value_valid(self):
        """Test get_value with an valid key."""
        test = self.CommandInfo.get_value(
            self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, self.info)
        self.assertEqual(test.command_name, self.command_name)

    def test_get_value_invalid_key(self):
        """Test get_value with an invalid key."""
        test = self.CommandInfo.get_value(
            'test2', 'test2')
        self.assertIsNone(test)

    def test_set_value_new(self):
        """Test set_value when value doesn't exist."""
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
        """Test set_value when value exists."""
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
        """Test remove_value when value exists."""
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
        """Test remove_value when value doesn't exist."""
        test = self.CommandInfo.get_value(
            self.command_name, 'teste2')
        self.assertIsNone(test)
        self.assertFalse(
            self.CommandInfo.remove_value(
                self.command_name, 'teste2'))

class TestUtilsTime(unittest.TestCase):
    """Test Request functionalities."""

    def test_UM_DIA_EM_SEGUNDOS(self):
        """Test total seconds at UM_DIA_EM_SEGUNDOS."""
        self.assertEqual(
            utils.time.UM_DIA_EM_SEGUNDOS, 60 * 60 * 24,
        )

    def test_UMA_HORA_EM_SEGUNDOS(self):
        """Test total seconds at UMA_HORA_EM_SEGUNDOS."""
        self.assertEqual(
            utils.time.UMA_HORA_EM_SEGUNDOS, 60 * 60,
        )

    def test_UMA_SEMANA_EM_SEGUNDOS(self):
        """Test total seconds at UMA_SEMANA_EM_SEGUNDOS."""
        self.assertEqual(
            utils.time.UMA_SEMANA_EM_SEGUNDOS, 60 * 60 * 24 * 7,
        )

class TestUtilsRequest(unittest.TestCase):
    """Test Request functionalities."""

    def test_get_html_soup(self):
        """Test get_html_soup."""
        soup = utils.request.get_html_soup('https://google.com')
        self.assertIn('Google', soup.text)

        soup = utils.request.get_html_soup('test')
        self.assertIsNone(soup)

    def test_get_json(self):
        """Test get_json."""
        result = utils.request.get_json('test')
        self.assertIsInstance(result, dict)

    def test_telegram_send_photo(self):
        """Test telegram_send_photo."""
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
        """Test telegram_send_message."""
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
    """Test CommandBase functionalities."""

    @classmethod
    def setUpClass(cls):
        """Mock a command."""
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
        """Remove mocked values inside Cache and CommandInfo."""
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(
            self.name, self.message)

    def tearDown(self):
        """Remove mocked values inside Cache and CommandInfo."""
        utils.database.Cache.remove_value(self.name)
        utils.database.CommandInfo.remove_value(
            self.name, self.message)

    def test_set_info(self):
        """Test set_info."""
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
        """Test get_info."""
        command = self.Command()

        info = command.get_info(self.message)
        self.assertIsNone(info)

        text = 'test2'
        command.set_info(self.message, text)
        info = command.get_info(self.message)
        self.assertIsNotNone(info)
        self.assertEqual(info, text)

    def test_remove_info(self):
        """Test remove_info."""
        command = self.Command()
        removed = command.remove_info(self.message)
        self.assertFalse(removed)

        text = 'test2'
        command.set_info(self.message, text)

        removed = command.remove_info(self.message)
        self.assertTrue(removed)

    def test_get_result_cache(self):
        """Test get_result with cached results."""
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
        """Test get_result without cached results."""
        command = self.Command()
        result = command.get_result()
        self.assertEqual(result, self.message)

    def test_get_schedule(self):
        """Test get_schedule."""
        command = self.Command()
        schedule = command.get_schedule()
        self.assertIsNone(schedule)

        command_sched = self.Command(5)
        schedule = command_sched.get_schedule()
        self.assertTrue(
            isinstance(schedule, utils.schedule.Schedule))

    def test_function_not_implemented(self):
        """Test CommandBase function."""
        with self.assertRaises(NotImplementedError):
            utils.command_base.CommandBase(None, None, None, None).function()

    def test_function(self):
        """Test function."""
        self.assertEqual(self.Command().function(), self.message)

    def test_init(self):
        """Test initialization."""
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
        """Test do_command."""
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
    """Test utils.schedule functionality."""

    def test_Schedule(self):
        """Test Schedule initialization."""
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
    """Test about functionalities."""

    def test_function(self):
        """Test about function."""
        result = commands.about.About().function()
        self.assertIn('comunidade', result)
        self.assertIn('contribuir', result)

class TestPackt(unittest.TestCase):
    """Test packt functionalities."""

    def test_function(self):
        """Test packt function."""
        result = commands.packt.Packt().function()
        self.assertIn('Livro', result)
        self.assertIn('gratuito', result)
        self.assertIn(
            'https://www.packtpub.com/free-learning', result)

class TestLinks(unittest.TestCase):
    """Test links functionalities."""

    def test_function(self):
        """Test links function."""
        result = commands.links.Links().function()
        self.assertIn('links', result)
        self.assertIn('Python', result)

class TestMemes(unittest.TestCase):
    """Test memes functionalities."""

    def test_get_url_image_vida_programador(self):
        """Test get_url_image_vida_programador."""
        pass

    def test_get_url_image_turnoff_us(self):
        """Test get_url_image_turnoff."""
        pass

    def test_get_random_meme_image(self):
        """Test get_random_meme_image."""
        pass

class TestNews(unittest.TestCase):
    """Test news functionalities."""

    def test_function(self):
        """Test news function."""
        result = commands.news.News().function()
        self.assertIn('notícia', result)
        self.assertIn('http', result)

class TestProjects(unittest.TestCase):
    """Test projects functionalities."""

    def test_function(self):
        """Test projects function."""
        result = commands.projects.Projects().function()
        self.assertIn('projetos', result)
        self.assertIn('http', result)

class TestSay(unittest.TestCase):
    """Test say functionalities."""

    def test_function(self):
        """Test say function."""
        result = commands.say.Say().function()
        self.assertEqual('', result)

        result = commands.say.Say().function(mock_update('test'))
        self.assertEqual('test', result)

class TestUdemy(unittest.TestCase):
    """Test udemy functionalities."""

    def test_function(self):
        """Test udemy function."""
        result = commands.udemy.Udemy().function()
        self.assertIn('Udemy', result)
        self.assertIn('http', result)

class TestFAQ(unittest.TestCase):
    """Test FAQ functionalities."""

    def test_function(self):
        """Test FAQ function."""
        result = commands.faq.FAQ().function()
        self.assertIn('O que é Python?', result)
        self.assertIn('https://www.python.org/dev/peps/pep-0008', result)

class TestHelp(unittest.TestCase):
    """Test help functionalities."""

    def test_function(self):
        """Test help function."""
        result = commands.help.Help().function()
        self.assertIn('/help', result)
        self.assertIn('/udemy', result)
        self.assertIn('/news', result)

if __name__ == '__main__':
    unittest.main()
