import unittest

from .. import schedules
from ..utils.command import get_commands

'''
# TODO mockar apscheduler
# TODO refatorar tests
# TODO implementar novos
'''
class TestSchedules(unittest.TestCase):
    """Test run_schedules module."""

    def test_get_schedule_list(self):
        """Test get_schedule_list."""
        sched_list = schedules.get_schedule_list()
        bot_commands = get_commands()
        schedules_count = 0
        for bot_command in bot_commands:
            if bot_command.get_schedule():
                schedules_count += 1

        self.assertEqual(schedules_count, len(sched_list))

    def test_get_scheduler(self):
        pass
        '''
        def get_scheduler():
        """Get scheduler from APScheduler."""
        config = {
            "apscheduler.jobstores.default": {
                "type": "sqlalchemy",
                "url": DATABASE_URL,
            },
        }
        return BackgroundScheduler(config, daemon=True)
        '''

    def test_add_schedules(self):
        pass
        '''
        def add_schedule(sched, function, args, jitter):
    """Add a schedule to the scheduler."""
    name = args[0].name
    trigger = IntervalTrigger(seconds=args[0].interval, jitter=jitter,)
    misfire_grace_time = UM_DIA_EM_SEGUNDOS * 14
    job_data = {
        "func": function,
        "trigger": trigger,
        "args": args,
        "id": name,
        "coalesce": True,
        "misfire_grace_time": misfire_grace_time,
        "replace_existing": False,
    }
    try:
        sched.add_job(**job_data)
    except:
        logger.info(f"Updating {name}")
        job = sched.get_job(name)
        job_interval = job.trigger.interval
        if job_interval != trigger.interval:  # alterar tudo
            job_data["replace_existing"] = True
            sched.add_job(**job_data)
        else:  # manter trigger antigo
            job = sched.get_job(name)
            job.modify(
                func=function,
                args=args,
                misfire_grace_time=misfire_grace_time,
                coalesce=True,
            )
        '''

    def test_run_schedules(self):
        pass
        '''
        def run_schedule(schedule):
            """Run schedule and sends messages."""
            result = None
            if schedule.format == "text":
                result = telegram_send_message(schedule.function(), TARGET_CHAT_ID)
            elif schedule.format == "photo":
                result = telegram_send_photo(schedule.function(), TARGET_CHAT_ID)
            return result
        '''

    def test_main(self):
        '''
        def main():
            """Run bot schedules."""
            schedule_list = get_schedule_list()
            if schedule_list:
                sched = get_scheduler()
                logger.info("Checking jobs")
                sched.start()
                sched.pause()

                for schedule in schedule_list:
                    add_schedule(
                        sched,
                        run_schedule,
                        args=[schedule],
                        jitter=UMA_HORA_EM_SEGUNDOS // 20,
                    )
                logger.info("Resuming Scheduler")
                sched.resume()
                try:
                    while True:
                        time.sleep(2)
                except (KeyboardInterrupt, SystemExit):
                    sched.shutdown()
        '''
