import unittest
from unittest.mock import Mock, patch

import datetime

from utils import database

"""
mockar acesso aos banco nos modelos peewee
isolar testes mockando módulos
remover duplicidade

28.54s

Cache.get(cls.key == key) mock return cache_item
Cache.create mock return cache_item
cache_item.save()
cache_item.delete_instance


CommandInfo.get mock return info
CommandInfo.create mock return info 
info.save
info.delete_instance
"""


class TestUtilsDatabaseCache(unittest.TestCase):
    """Test Cache functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the Cache object."""
        cls.key = "test_key"
        cls.text = "test"
        cls.expire_time = 0

    @patch("utils.database.Cache.get")
    def test_get_value_valid(self, get):
        """Test get_value when value doesn't exist."""
        cached_item = Mock()
        cached_item.key = self.key
        cached_item.result = self.text
        cached_item.expire_time = self.expire_time

        get.return_value = cached_item

        test = database.Cache.get_value(self.key)
        get.assert_called()
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertEqual(test.expire_time, self.expire_time)

    @patch("utils.database.Cache.get")
    def test_get_value_invalid_key(self, get):
        """Test get_value when value doesn't exist."""
        get.return_value = None
        test = database.Cache.get_value("test")
        self.assertIsNone(test)

    @patch("utils.database.Cache.get")
    def test_get_value_invalid_expire(self, get):
        """Test get_value when value is expired."""
        get.return_value = None
        test = database.Cache.get_value(self.key)
        expire_approx = datetime.datetime.now()

        get.assert_called_once()

        expression = get.call_args[0][0]
        self.assertEqual(expression.op, "AND")

        expression_l = expression.lhs
        self.assertEqual(expression_l.op, "=")
        self.assertEqual(expression_l.lhs, database.Cache.key)
        self.assertEqual(expression_l.rhs, self.key)

        expression_r = expression.rhs
        self.assertEqual(expression_r.op, ">")
        self.assertEqual(expression_r.lhs, database.Cache.expire_time)

        time_diff = (expire_approx - expression_r.rhs).total_seconds()
        self.assertLessEqual(time_diff, 1)

        self.assertIsNone(test)

    @patch("utils.database.Cache.create")
    @patch("utils.database.Cache.get")
    def test_set_value_new(self, get, create):
        """Test set_value when value doesn't exist."""
        get.return_value = None
        expire_approx = datetime.datetime.now() + datetime.timedelta(
            seconds=self.expire_time
        )
        cached_item = Mock()
        cached_item.key = self.key
        cached_item.result = self.text
        cached_item.expire_time = expire_approx
        create.return_value = cached_item

        test = database.Cache.set_value(self.key, self.text, self.expire_time)
        kwargs = create.call_args[1]
        self.assertEqual(kwargs["key"], self.key)
        self.assertEqual(kwargs["result"], self.text)
        time_diff = (kwargs["expire_time"] - expire_approx).total_seconds()
        self.assertLessEqual(time_diff, 1)

        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertEqual(test.expire_time, expire_approx)

    @patch("utils.database.Cache.create")
    @patch("utils.database.Cache.get")
    def test_set_value_old(self, get, create):
        """Test set_value when value exists."""
        cached_item = Mock()
        cached_item.key = self.key
        cached_item.result = self.text
        cached_item.expire_time = self.expire_time
        cached_item.save.return_value = cached_item
        get.return_value = cached_item

        test = database.Cache.set_value(self.key, self.text, self.expire_time)
        expire_approx = datetime.datetime.now() + datetime.timedelta(
            seconds=self.expire_time
        )
        create.assert_not_called()
        cached_item.save.assert_called_once()

        self.assertEqual(self.key, test.key)
        self.assertEqual(self.text, test.result)
        self.assertNotEqual(self.expire_time, test.expire_time)
        time_diff = (expire_approx - test.expire_time).total_seconds()
        self.assertEqual(time_diff, 0)

    @patch("utils.database.Cache.get")
    def test_remove_value_exist(self, get):
        """Test remove_value when value exists."""
        cached_item = Mock()
        cached_item.delete_instance.return_value = True
        get.return_value = cached_item
        self.assertTrue(database.Cache.remove_value(self.key))
        cached_item.delete_instance.assert_called()

        expression = get.call_args[0][0]
        self.assertEqual(expression.op, "=")
        self.assertEqual(expression.lhs, database.Cache.key)
        self.assertEqual(expression.rhs, self.key)

    @patch("utils.database.Cache.get")
    def test_remove_value_no_exist(self, get):
        """Test remove_value when value doesn't exist."""
        get.return_value = None
        self.assertFalse(database.Cache.remove_value(self.key))


class TestUtilsDatabaseCommandInfo(unittest.TestCase):
    """Test CommandInfo functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the Cache object."""
        cls.command_name = "test"
        cls.key = "test"
        cls.info = "test"

    @patch("utils.database.CommandInfo.get")
    def test_get_value_valid(self, get):
        """Test get_value with an valid key."""
        info_mock = Mock()
        info_mock.command_name = self.command_name
        info_mock.info = self.info
        info_mock.key = self.key
        get.return_value = info_mock

        test = database.CommandInfo.get_value(self.command_name, self.key)

        expression = get.call_args[0][0]
        self.assertEqual(expression.op, "AND")

        expression_l = expression.lhs
        self.assertEqual(expression_l.op, "=")
        self.assertEqual(expression_l.lhs, database.CommandInfo.command_name)
        self.assertEqual(expression_l.rhs, self.command_name)

        expression_r = expression.rhs
        self.assertEqual(expression_r.op, "=")
        self.assertEqual(expression_r.lhs, database.CommandInfo.key)
        self.assertEqual(expression_r.rhs, self.key)

        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, self.info)
        self.assertEqual(test.command_name, self.command_name)

    @patch("utils.database.CommandInfo.get")
    def test_get_value_invalid_key(self, get):
        """Test get_value with an invalid key."""
        get.return_value = None
        test = database.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNone(test)

    @patch("utils.database.CommandInfo.create")
    @patch("utils.database.CommandInfo.get")
    def test_set_value_no_exists(self, get, create):
        """Test set_value when value doesn't exist."""
        get.return_value = None
        mock_info = Mock()
        mock_info.command_name = self.command_name
        mock_info.key = self.key
        mock_info.info = self.info
        create.return_value = mock_info

        test = database.CommandInfo.set_value(
            self.command_name, self.key, self.info
        )
        create.assert_called_with(
            command_name=self.command_name, key=self.key, info=self.info,
        )

        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, self.info)
        self.assertEqual(test.command_name, self.command_name)

    @patch("utils.database.CommandInfo.create")
    @patch("utils.database.CommandInfo.get")
    def test_set_value_exists(self, get, create):
        """Test set_value when value exists."""
        mock_info = Mock()
        mock_info.command_name = self.command_name
        mock_info.key = self.key
        mock_info.info = self.info
        mock_info.save.return_value = mock_info
        get.return_value = mock_info

        test = database.CommandInfo.set_value(
            self.command_name, self.key, self.info
        )
        create.assert_not_called()
        mock_info.save.assert_called_once()

        self.assertEqual(self.key, test.key)
        self.assertEqual(self.info, test.info)
        self.assertEqual(self.command_name, test.command_name)

    @patch("utils.database.CommandInfo.get")
    def test_remove_value_exists(self, get):
        """Test remove_value when value exists."""
        mock_info = Mock()
        mock_info.delete_instance.return_value = True
        get.return_value = mock_info
        self.assertTrue(
            database.CommandInfo.remove_value(self.command_name, self.key)
        )
        mock_info.delete_instance.assert_called()

        expression = get.call_args[0][0]
        self.assertEqual(expression.op, "AND")

        expression_l = expression.lhs
        self.assertEqual(expression_l.op, "=")
        self.assertEqual(expression_l.lhs, database.CommandInfo.command_name)
        self.assertEqual(expression_l.rhs, self.command_name)

        expression_r = expression.rhs
        self.assertEqual(expression_r.op, "=")
        self.assertEqual(expression_r.lhs, database.CommandInfo.key)
        self.assertEqual(expression_r.rhs, self.key)

    @patch("utils.database.CommandInfo.get")
    def test_remove_value_no_exist(self, get):
        """Test remove_value when value doesn't exist."""
        get.return_value = None
        self.assertFalse(
            database.CommandInfo.remove_value(self.command_name, self.key)
        )
