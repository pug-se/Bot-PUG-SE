"""Run bot schedules."""

import time

from utils.schedule_manager import (
    get_schedule_list,
    get_scheduler,
    add_schedule,
    run_schedule,
)
from utils.logging import schedule_logger
from utils.time import UMA_HORA_EM_SEGUNDOS

logger = schedule_logger


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


if __name__ == "__main__":
    main()
