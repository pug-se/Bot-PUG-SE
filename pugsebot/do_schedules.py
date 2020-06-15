import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import ConflictingIdError

import os

from bot import target_chat_id, token
import commands

import logging
logger = logging.getLogger('apscheduler.scheduler')

database_url = os.environ.get('DATABASE_URL')

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

def send_content(schedule, chat_id):
    result = None
    if schedule.format == 'text':
        result = send_message(schedule.function(), chat_id)
    elif schedule.format == 'photo':
        result = send_photo(schedule.function(), chat_id)
    return result

def add_schedule(sched, function, args, jitter):
    name = args[0].name
    trigger = IntervalTrigger(seconds=args[0].interval, jitter=jitter)
    try:
        sched.add_job(
        function,
        trigger,
        args=args,
        id=name,
    )
    except ConflictingIdError:
        logger.info(f'Updating {name}')
        job = sched.get_job(name)
        job.modify(func=function)
        job_interval = job.trigger.interval
        if job_interval != trigger.interval:
            job.reschedule(trigger)

def get_scheduler(background=False, url=database_url):
    config = {
        'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': url,
        },
    }
    if background:
        return BackgroundScheduler(config)
    return BlockingScheduler(config)

if __name__ == '__main__':
    schedule_list = get_schedule_list()
    if schedule_list:
        logger.info('Checking jobs')
        sched = get_scheduler(background=True)
        sched.start()
        for schedule in schedule_list:
            add_schedule(
                sched,
                send_content,
                args=[schedule, target_chat_id],
                jitter=0#UMA_HORA_EM_SEGUNDOS // 20,
            )
        sched.shutdown()
        logger.info('Starting Scheduler')
        sched = get_scheduler()
        sched.start()
