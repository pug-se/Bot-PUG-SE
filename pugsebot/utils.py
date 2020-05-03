import requests
from bs4 import BeautifulSoup
import re
import threading

import logging

import warnings
warnings.filterwarnings("ignore")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'\
    ' AppleWebKit/537.36 (KHTML, like Gecko)'\
    ' Chrome/39.0.2171.95 Safari/537.36'}

def get_html_soup(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text)