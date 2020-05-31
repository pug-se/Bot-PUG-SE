import logging
import threading
import time

import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'\
    ' AppleWebKit/537.36 (KHTML, like Gecko)'\
    ' Chrome/39.0.2171.95 Safari/537.36'}

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

class Schedule:
    def __init__(self, job, interval):
        self.job = job
        self.interval = interval
        self.thread = None
        self.logger = logging.getLogger('Schedule')

    def run_thread(self, unused):
        while True:
            time.sleep(self.interval)
            try:
                name = self.job.__name__
                self.logger.info(
                    f'{name} running')
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
        self.logger = logging.getLogger('ScheduleManager')
        self.schedules = {}

    def add_schedule(self, job, interval):
        name = job.__name__
        self.logger.info(
            f'Scheduling {name} with {interval/3600} hours of interval...')
        if name not in self.schedules:
            schedule = Schedule(job, interval)
            self.schedules[name] = schedule
            schedule.start()