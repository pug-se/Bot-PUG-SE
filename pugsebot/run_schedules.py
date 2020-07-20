"""Schedules and runs funcions defined by commands
 and sends messages with the results.

The messages will be sent to the Group
 defined by utils.environment.TARGET_CHAT_ID
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import time

from utils.environment import DATABASE_URL, TARGET_CHAT_ID
from utils.time import UM_DIA_EM_SEGUNDOS, UMA_HORA_EM_SEGUNDOS
from utils.logging import schedule_logger
from utils.request import telegram_send_message, telegram_send_photo

import commands

logger = schedule_logger

def _get_schedule_list():
    """Get list of schedules from all comands."""

    schedules = [
        command.get_schedule() for command in commands.command_list
    ]
    return [schedule for schedule in schedules if schedule]

def _get_scheduler():
    """Get scheduler from APScheduler."""

    config = {
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': DATABASE_URL,
        },
    }
    return BackgroundScheduler(config, daemon=True)

def _add_schedule(sched, function, args, jitter):
    """Adds a schedule to the scheduler."""

    name = args[0].name
    trigger = IntervalTrigger(
        seconds=args[0].interval, jitter=jitter,
    )
    misfire_grace_time = UM_DIA_EM_SEGUNDOS * 14
    job_data = {
        'func': function, 'trigger': trigger,
        'args': args, 'id': name,
        'coalesce': True,
        'misfire_grace_time': misfire_grace_time,
        'replace_existing': False,
    }
    try:
        sched.add_job(**job_data)
    except:
        logger.info(f'Updating {name}')
        job = sched.get_job(name)
        job_interval = job.trigger.interval
        if job_interval != trigger.interval:  # alterar tudo
            job_data['replace_existing'] = True
            sched.add_job(**job_data)
        else:  # manter trigger antigo
            job = sched.get_job(name)
            job.modify(
                func=function, args=args,
                misfire_grace_time=misfire_grace_time,
                coalesce=True,
            )

def _run_schedule(schedule):
    """Runs schedule and sends messages."""

    result = None
    if schedule.format == 'text':
        result = telegram_send_message(schedule.function(), TARGET_CHAT_ID)
    elif schedule.format == 'photo':
        result = telegram_send_photo(schedule.function(), TARGET_CHAT_ID)
    return result

if __name__ == '__main__':
    schedule_list = _get_schedule_list()
    if schedule_list:
        sched = _get_scheduler()
        logger.info('Checking jobs')
        sched.start()
        sched.pause()

        for schedule in schedule_list:
            _add_schedule(
                sched,
                _run_schedule,
                args=[schedule],
                jitter=UMA_HORA_EM_SEGUNDOS // 20,
            )
        logger.info('Resuming Scheduler')
        sched.resume()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            sched.shutdown()
