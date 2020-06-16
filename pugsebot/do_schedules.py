import requests

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import ConflictingIdError

import os
import time

from bot import target_chat_id, token
import commands
from utils import UM_DIA_EM_SEGUNDOS, UMA_HORA_EM_SEGUNDOS

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

def add_job(data):
    sched.add_job(
        data['function'],
        data['trigger'],
        args=data['args'],
        id=data['name'],
        misfire_grace_time=data['misfire_grace_time'],
        coalesce=True,
        replace_existing=data['replace_existing'],
    )

def add_schedule(sched, function, args, jitter):
    name = args[0].name
    trigger = IntervalTrigger(seconds=args[0].interval, jitter=jitter)
    misfire_grace_time = UM_DIA_EM_SEGUNDOS * 14
    job_data = {
        'sched':sched, 'function':function, 'trigger':trigger,
        'args':args, 'name':name,
        'misfire_grace_time':misfire_grace_time,
        'replace_existing':False,
    }
    try:
        add_job(
            job_data
        )
    except ConflictingIdError:
        logger.info(f'Updating {name}')
        job = sched.get_job(name)
        job_interval = job.trigger.interval
        if job_interval != trigger.interval: # alterar tudo
            job_data['replace_existing'] = True
            add_job(
                job_data
            )
        else: # manter trigger antigo
            job = sched.get_job(name)
            job.modify(func=function)
            job.modify(func=function)
            job.modify(args=args)
            job.modify(misfire_grace_time=misfire_grace_time)
            job.modify(coalesce=True)

def get_scheduler(url=database_url):
    config = {
        'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': url,
        },
    }
    return BackgroundScheduler(config, daemon=True)

if __name__ == '__main__':
    schedule_list = get_schedule_list()
    if schedule_list:
        sched = get_scheduler()
        logger.info('Checking jobs')
        sched.start()
        sched.pause()
        for schedule in schedule_list:
            add_schedule(
                sched,
                send_content,
                args=[schedule, target_chat_id],
                jitter=UMA_HORA_EM_SEGUNDOS // 20,
            )
        logger.info('Resuming Scheduler')
        sched.resume()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            sched.shutdown()
