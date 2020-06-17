import abc
import json
import os

import requests
from bs4 import BeautifulSoup
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'\
    ' AppleWebKit/537.36 (KHTML, like Gecko)'\
    ' Chrome/39.0.2171.95 Safari/537.36'}

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24
UMA_HORA_EM_SEGUNDOS = 60 * 60

def get_html_soup(url):
    soup = None
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        pass
    return soup

def get_json(url):
    result_dict = {}
    try:
        r = requests.get(url, headers=headers)
        result_dict = json.loads(r.text)
    except:
        pass
    return result_dict

class Cache():
    cache_manager = None
    cache_log = logging.getLogger('Cache')
    def __init__(self, name, expire):
        self.init_cache_manager()
        if expire is not None:
            self.cache = self.cache_manager.get_cache(name, expire=expire)
        else:
            self.cache = None

    @classmethod
    def init_cache_manager(cls):
        if cls.cache_manager is None:
            if 'DATABASE_URL' in os.environ:
                cache_opts = {
                    'cache.type': 'ext:database',
                    'cache.url': os.environ['DATABASE_URL'],
                    'cache.lock_dir': 'lock'
                }
            else:
                cache_opts = {
                    'cache.type': 'memory',
                    'cache.lock_dir': 'lock'
                }

            cls.cache_manager = CacheManager(
                **parse_cache_config_options(cache_opts)
            )

    def get(self, key):
        if (self.cache is None) or (not self.cache.has_key(key)):
            return None
        self.cache_log.info(f'Hit for key {key}')
        return self.cache.get(key)

    def set(self, key, value):
        if self.cache is not None:
            self.cache.set_value(key, value)

    def clear(self):
        self.cache.clear()

class Schedule():
    def __init__(self, name, function, message_type, interval):
        self.name = name
        self.function = function
        self.interval = interval
        if "photo" in message_type:
            self.format = 'photo'
        else:
            self.format = 'text'

class Command():
    def __init__(
        self,
        name,
        help_text,
        reply_function_name,
        schedule_interval,
        expire=None,
    ):
        self.name = name
        self.help_text = help_text
        self.reply_function_name = reply_function_name
        self.interval = schedule_interval
        self.cache = Cache(name, expire)

    @abc.abstractmethod
    def function(self, update=None, context=None):
        raise NotImplementedError

    def get_result(self, update=None, context=None):
        cached_value = self.cache.get(self.name)
        if cached_value is None:
            cached_value = self.function(update, context)
            self.cache.set(self.name, cached_value)
        return cached_value

    def do_command(self, update=None, context=None):
        return {
            'update': update,
            'response': self.get_result(update, context),
        }

    def get_schedule(self):
        if self.interval:
            return Schedule(
                self.name + '_function',
                self.get_result,
                self.reply_function_name,
                self.interval,
            )
        return None
