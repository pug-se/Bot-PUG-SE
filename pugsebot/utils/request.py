"""Define utilites for requesting Internet data."""

import requests
from bs4 import BeautifulSoup
import json

from .environment import TOKEN

_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
    ' AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/39.0.2171.95 Safari/537.36'
}

def get_html_soup(url):
    """Get a Beautiful Soup object from a Url."""
    soup = None
    try:
        r = requests.get(url, headers=_headers)
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        pass
    return soup

def get_json(url):
    """Get a JSON object from a Url."""
    result_dict = {}
    try:
        r = requests.get(url, headers=_headers)
        result_dict = json.loads(r.text)
    except:
        pass
    return result_dict

base = f'https://api.telegram.org/bot{TOKEN}/'

def telegram_send_photo(photo, chat_id):
    """Send a photo to a Telegram group."""
    data = {
        'chat_id': chat_id,
        'photo': photo,
    }
    return requests.post(base + 'sendPhoto', data=data)

def telegram_send_message(text, chat_id):
    """Send a text message to a Telegram group."""
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    return requests.post(base + 'sendMessage', data=data)
