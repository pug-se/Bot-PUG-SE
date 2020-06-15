import abc
import json

import requests
from bs4 import BeautifulSoup

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
    ):
        self.name = name
        self.help_text = help_text
        self.reply_function_name = reply_function_name
        self.interval = schedule_interval

    def do_command(self, update=None, context=None):
        return {
            'update': update,
            'response': self.function(update, context),
        }

    @abc.abstractmethod
    def function(self, update=None, context=None):
        raise NotImplementedError

    def get_schedule(self):
        if self.interval:
            return Schedule(
                self.name + '_function',
                self.function,
                self.reply_function_name,
                self.interval,
            )
        return None
