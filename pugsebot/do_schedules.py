import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot import target_chat_id, token
from utils import UMA_HORA_EM_SEGUNDOS
# pylint: disable=C0411
import commands

def get_schedule_list():
    schedules = [
        command.get_schedule() for command in commands.command_list
    ]
    return [schedule for schedule in schedules if schedule]

base = f'https://api.telegram.org/bot{token}/'

def send_photo(photo, chat_id):
    data = {
        'chat_id': chat_id,
        'photo': photo,
    }
    r = requests.post(base + 'sendPhoto', data=data)
    return r

def send_message(text, chat_id):
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    r = requests.post(base + 'sendMessage', data=data)
    return r

# pylint: disable=W0621
def send_content(schedule, chat_id):
    result = None
    if schedule.format == 'text':
        result = send_message(schedule.function(), chat_id)
    elif schedule.format == 'photo':
        result = send_photo(schedule.function(), chat_id)
    return result

# pylint: disable=W0621
def add_schedule(sched, function, args, interval, jitter):
    sched.add_job(
        function,
        IntervalTrigger(seconds=interval, jitter=jitter),
        args=args,
    )

if __name__ == '__main__':
    schedule_list = get_schedule_list()
    if schedule_list:
        sched = BlockingScheduler()
        for schedule in schedule_list:
            add_schedule(
                sched,
                send_content,
                args=[schedule, target_chat_id],
                interval=schedule.interval,
                jitter=UMA_HORA_EM_SEGUNDOS * 3
            )
        sched.start()
