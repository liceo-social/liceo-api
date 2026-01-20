from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, Sequence, TypeVar, override

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .utils import singleton


class Job(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


@dataclass
class IntervalJob(Job):
    name: str
    seconds: int = 60

    @override
    def get_name(self):
        return self.name


T = TypeVar("T")


@dataclass
class JobCollection(Generic[T]):
    jobs: List[T]


@singleton
class Scheduler:
    _scheduler: AsyncIOScheduler

    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    def start(self):
        self._scheduler.start()

    def add_job(
        self,
        func: Any | None = None,
        trigger: Any | None = None,
        args: Any | None = None,
        kwargs: Any | None = None,
        **trigger_args,
    ):
        self._scheduler.add_job(
            func, trigger=trigger, args=args, kwargs=kwargs, **trigger_args
        )

    def add_interval_job(self, job: IntervalJob):
        self._scheduler.add_job(
            job.execute, "interval", seconds=job.seconds, name=job.name
        )

    def add_job_collections(self, job_cols: Sequence[JobCollection]):
        for collection in job_cols:
            for job in collection.jobs:
                self.add_interval_job(job)

    def shutdown(self):
        self._scheduler.shutdown()


class SchedulerSingleton:
    @staticmethod
    def instance():
        return Scheduler()
