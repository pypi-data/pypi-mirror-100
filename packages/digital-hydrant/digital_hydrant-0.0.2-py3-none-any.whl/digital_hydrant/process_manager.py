from multiprocessing import Process
from time import sleep
from datetime import datetime
import functools
import importlib
import traceback
import schedule

from digital_hydrant import logging
from digital_hydrant.collector_queue import CollectorQueue
import digital_hydrant.config


def now():
    return datetime.timestamp(datetime.now())


days_of_the_week = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


class ProcessManager:
    scheduler = None

    def __init__(self, manager_name=None, db_name=None):
        self.manager_name = manager_name
        self.logger = logging.getLogger(f"{__name__}-{self.manager_name}")
        self.queue = CollectorQueue(db_name=db_name)
        self.process_details = {}
        self.jobs = {}
        self.job_schedules = {}
        self.scheduler = schedule.Scheduler()

    def error_wrapper(self, f, name):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                err_details = traceback.format_exc()
                err_details = err_details.replace("'", '"')
                self.logger.error(f"Caught error: {e}")

                self.queue.put(
                    **{
                        "type": "error",
                        "payload": {"error": err_details, "process": name},
                        "timestamp": now() * 1000,
                    }
                )
                raise

        return wrapped

    def add_process(self, name, target, args=()):
        self.process_details[name] = {
            "target": self.error_wrapper(target, name),
            "args": args,
        }

    def is_scheduled(self, name):
        return name in self.jobs and isinstance(self.jobs[name], schedule.Job)

    def run_job(self, name):
        details = self.process_details[name]
        p = Process(
            target=details["target"],
            args=details["args"],
            name=name,
        )
        p.start()

    def run_job_once(self, name):
        self.run_job(name)

        return schedule.CancelJob

    # cron string:
    # <day of week(1-7)> <days> <hours> <minutes> <seconds>
    # whichever value is populated first will be read as "every <value> <interval>" and the remaining values will be combined and read as "at <values>"
    # example: * 10 2 30 0 = "every 10 days at 2:30:00"
    # example: 5 * * 30 45 = "every thursday at 0:30:45"
    # days of the week values start on Sunday (i.e 1 = Sun, 7 = Sat)
    # for strings with the day of the week populated, the day value will be ignored
    def schedule(self, name, cron):
        parts = cron.split()
        if len(parts) != 5:
            return
        dow, day, hour, minute, second = [
            part.zfill(2) if part != "*" else part for part in parts
        ]

        job = None

        if dow != "*":
            hour = "00" if hour == "*" else hour
            minute = "00" if minute == "*" else minute
            second = "00" if second == "*" else second

            dow_index = int(dow) - 1
            if dow_index < 0 or dow_index > 6:
                return

            job = (
                getattr(self.scheduler.every(), days_of_the_week[dow_index])
                .at(f"{hour}:{minute}:{second}")
                .do(self.run_job, name)
            )
        elif day != "*":
            hour = "00" if hour == "*" else hour
            minute = "00" if minute == "*" else minute
            second = "00" if second == "*" else second
            job = (
                self.scheduler.every(int(day))
                .days.at(f"{hour}:{minute}:{second}")
                .do(self.run_job, name)
            )
        elif hour != "*":
            minute = "00" if minute == "*" else minute
            second = "00" if second == "*" else second
            job = (
                self.scheduler.every(int(hour))
                .hours.at(f"{minute}:{second}")
                .do(self.run_job, name)
            )
        elif minute != "*":
            second = "00" if second == "*" else second
            job = (
                self.scheduler.every(int(minute))
                .minutes.at(f":{second}")
                .do(self.run_job, name)
            )
        elif second != "*":
            job = self.scheduler.every(int(second)).seconds.do(self.run_job, name)
        else:
            job = self.scheduler.every().second.do(self.run_job_once, name)

        self.logger.info(f"Scheduling {name} with {cron}")
        self.jobs[name] = job
        self.job_schedules[name] = cron

    def manage(self):
        while True:
            self.scheduler.run_pending()

            importlib.reload(digital_hydrant.config)
            schedule_wait = digital_hydrant.config.config.getint(
                "ping", "wait", fallback=30
            )
            self.allowed_time = schedule_wait * 2

            active = []

            for name in self.process_details.keys():
                enabled = digital_hydrant.config.config.getboolean(
                    name, "enabled", fallback=True
                )
                cron = digital_hydrant.config.config.get(
                    name, "schedule", fallback="* * * * *"
                )
                scheduled = self.is_scheduled(name)

                if enabled and not scheduled:
                    self.schedule(name, cron)
                elif not enabled and scheduled:
                    self.scheduler.cancel_job(self.jobs[name])
                    self.jobs.pop(name, None)
                elif (
                    enabled
                    and scheduled
                    and name in self.job_schedules
                    and cron != self.job_schedules[name]
                ):
                    self.scheduler.cancel_job(self.jobs[name])
                    self.schedule(name, cron)

                if scheduled:
                    active.append(name)

            self.logger.info(f"Active processes: {active}")
            sleep(5)
