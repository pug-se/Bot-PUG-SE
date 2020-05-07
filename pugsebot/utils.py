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

UM_DIA_EM_SEGUNDOS = 60 * 60 * 24

def get_html_soup(url):
    request = requests.get(url, headers=headers)
    return BeautifulSoup(request.text)

class ScheduleManager:
    def __init__(self):
        self.schedule_thread = None
        self.schedules = []

    def add_schedule(self, method):
        self.schedules.append(method)

    def run_thread(self, args):
        while True:
            for schedule in self.schedules:
                schedule()
            time.sleep(UM_DIA_EM_SEGUNDOS)

    def start_schedules(self):
        if self.schedule_thread:
            return
        self.schedule_thread = threading.Thread(
            target=self.run_thread,
            args=(self,),
            daemon=True,
        )
        self.schedule_thread.start()
