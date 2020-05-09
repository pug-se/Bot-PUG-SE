import logging
import threading
import time
import warnings

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'\
    ' AppleWebKit/537.36 (KHTML, like Gecko)'\
    ' Chrome/39.0.2171.95 Safari/537.36'}

def get_html_soup(url):
    request = requests.get(url, headers=headers)
    return BeautifulSoup(request.text)

class Schedule:
    def __init__(self, job, interval):
        self.job = job
        self.interval = interval
        self.thread = None
        self.logger = logging.getLogger('PUGSEBot')

    def run_thread(self, unused):
        while True:
            time.sleep(self.interval)
            try:
                self.job()
            except Exception as error:
                self.logger.error(error)

    def start(self):
        if self.thread:
            return
        self.thread = threading.Thread(
            target=self.run_thread,
            args=(self,),
            daemon=True,
        )
        self.thread.start()

class ScheduleManager:
    def __init__(self):
        self.schedules = {}

    def add_schedule(self, job, interval):
        name = job.__name__
        if name not in self.schedules:
            schedule = Schedule(job, interval)
            self.schedules[name] = schedule
            schedule.start()
