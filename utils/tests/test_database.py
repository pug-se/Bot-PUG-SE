import unittest

import datetime

from utils import database


class TestUtilsDatabaseCache(unittest.TestCase):
    """Test Cache functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the Cache object."""
        cls.Cache = database.Cache

    def setUp(self):
        """Cache mock information."""
        self.short_expire_time = datetime.datetime.now()
        expire_time = self.short_expire_time + datetime.timedelta(seconds=100)
        self.expire_time = expire_time
        self.text = "test"
        self.key = "test"
        try:
            # deletes test info created on unfinished testing sessions
            cached_test = self.Cache.get(self.Cache.key == self.key)
            cached_test.delete_instance()
        except:
            pass
        self.Cache.create(
            key=self.key, result=self.text, expire_time=self.expire_time,
        )

    def tearDown(self):
        """Delete cached information."""
        try:
            test = self.Cache.get(self.Cache.key == self.key)
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
        test = self.Cache.get_value("test2")
        self.assertIsNone(test)

    def test_get_value_invalid_expire(self):
        """Test get_value when value is expired."""
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        test.expire_time = self.short_expire_time
        test.save()
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_set_value_new(self):
        """Test set_value when value doesn't exist."""
        test = self.Cache.get_value(self.key)
        test.delete_instance()
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)
        new_time = 3
        test = self.Cache.set_value(self.key, self.text, new_time)
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, self.text)
        self.assertNotEqual(test.expire_time, self.expire_time)

    def test_set_value_old(self):
        """Test set_value when value exists."""
        new_time = 4
        new_text = self.text + "test"
        test = self.Cache.set_value(self.key, new_text, new_time)
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.result, new_text)
        self.assertNotEqual(test.expire_time, self.expire_time)

    def test_remove_value_exist(self):
        """Test remove_value when value exists."""
        test = self.Cache.get_value(self.key)
        self.assertIsNotNone(test)
        self.assertTrue(self.Cache.remove_value(self.key))
        test = self.Cache.get_value(self.key)
        self.assertIsNone(test)

    def test_remove_value_no_exist(self):
        """Test remove_value when value doesn't exist."""
        test = self.Cache.get_value("test2")
        self.assertIsNone(test)
        self.assertFalse(self.Cache.remove_value("test2"))
        test = self.Cache.get_value("test2")
        self.assertIsNone(test)


class TestUtilsDatabaseCommandInfo(unittest.TestCase):
    """Test CommandInfo functionalities."""

    @classmethod
    def setUpClass(cls):
        """Bind the CommandInfo object."""
        cls.CommandInfo = database.CommandInfo

    def setUp(self):
        """Store mock info."""
        self.command_name = "test"
        self.key = "test"
        self.info = "test"
        try:
            # deletes test info created on unfinished testing sessions
            info_test = self.CommandInfo.get(
                (self.CommandInfo.command_name == self.command_name)
                & (self.CommandInfo.key == self.key)
            )
            info_test.delete_instance()
        except:
            pass
        self.CommandInfo.create(
            command_name=self.command_name, key=self.key, info=self.info,
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
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, self.info)
        self.assertEqual(test.command_name, self.command_name)

    def test_get_value_invalid_key(self):
        """Test get_value with an invalid key."""
        test = self.CommandInfo.get_value("test2", "test2")
        self.assertIsNone(test)

    def test_set_value_deleted(self):
        """Test set_value when value doesn't exist."""
        test = self.CommandInfo.get_value(self.command_name, self.key)
        test.delete_instance()
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNone(test)

        new_info = "test3"
        test = self.CommandInfo.set_value(
            self.command_name, self.key, new_info
        )
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.command_name, self.command_name)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, new_info)

    def test_set_value_exists(self):
        """Test set_value when value exists."""
        new_info = "test3"
        test = self.CommandInfo.set_value(
            self.command_name, self.key, new_info
        )
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertEqual(test.command_name, self.command_name)
        self.assertEqual(test.key, self.key)
        self.assertEqual(test.info, new_info)

    def test_remove_value_exists(self):
        """Test remove_value when value exists."""
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNotNone(test)
        self.assertTrue(
            self.CommandInfo.remove_value(self.command_name, self.key)
        )
        test = self.CommandInfo.get_value(self.command_name, self.key)
        self.assertIsNone(test)

    def test_remove_value_no_exist(self):
        """Test remove_value when value doesn't exist."""
        test = self.CommandInfo.get_value(self.command_name, "teste2")
        self.assertIsNone(test)
        self.assertFalse(
            self.CommandInfo.remove_value(self.command_name, "teste2")
        )
