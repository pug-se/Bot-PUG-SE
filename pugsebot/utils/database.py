"""Defines Database related classes using a ORM"""

import datetime
import peewee
from playhouse.db_url import connect
from .environment import DATABASE_URL
from .logging import cache_logger

_db = connect(DATABASE_URL)

class Cache(peewee.Model):
    """
    Cache for commands

    Attibutes:

    key:
        key used to retrieve values

    result:
        value

    expire_time: 
        expiration time of the value    
    """
    key = peewee.CharField(unique=True)
    result = peewee.TextField(null=False)
    expire_time = peewee.DateTimeField(null=False)

    class Meta:
        database = _db

    @classmethod
    def set_value(cls, key, result, expire):
        """Sets a value inside the cache."""

        expire_time = datetime.datetime.now()
        expire_time += datetime.timedelta(seconds=expire)
        try:
            cached_item = cls.get(cls.key == key)
            cached_item.result = result
            cached_item.expire_time = expire_time
            cached_item.save()
        except:
            cached_item = cls.create(
                key=key, result=result,
                expire_time=expire_time,
            )
        return cached_item

    @classmethod
    def get_value(cls, key):
        """Gets a value inside the cache."""

        now = datetime.datetime.now()
        try:
            cached_result = cls.get(
                (cls.key == key)
                & (cls.expire_time > now)
            )
            cache_logger.info(
                f'Hit for key: {key}'
                f' and expire_time: {cached_result.expire_time}'
            )
            return cached_result
        except:
            return None

    @classmethod
    def remove_value(cls, key):
        """Removes a value inside the cache."""

        try:
            cached_value = cls.get(
                cls.key == key)
            cached_value.delete_instance()
            return True
        except:
            return False

class CommandInfo(peewee.Model):
    """Data that can be set and retrieved by commands
    
    Attributes:
    
    command_name:
        name of the command that sets/retrieves the data

    key:
        key used to retrieve the data
        
    info:
        a string data
    """

    command_name = peewee.CharField(null=False)
    key = peewee.CharField(null=False)
    info = peewee.TextField(null=False)

    class Meta:
        database = _db
        primary_key = peewee.CompositeKey(
            'command_name', 'key')

    @classmethod
    def set_value(cls, command_name, key, info):
        """Sets the data."""

        try:
            command_info = cls.get(
                (cls.command_name == command_name)
                & (cls.key == key)
            )
            command_info.info = info
            command_info.save()
        except:
            command_info = cls.create(
                command_name=command_name,
                key=key, info=info,
            )
        return command_info

    @classmethod
    def get_value(cls, command_name, key):
        """Gets the data."""

        try:
            command_info = cls.get(
                (cls.command_name == command_name)
                & (cls.key == key)
            )
            return command_info
        except:
            return None

    @classmethod
    def remove_value(cls, command_name, key):
        """Removes the data."""
        
        try:
            command_info = cls.get(
                (cls.command_name == command_name)
                & (cls.key == key)
            )
            command_info.delete_instance()
            return True
        except:
            return False

_db.connect()
_db.create_tables([Cache, CommandInfo])
