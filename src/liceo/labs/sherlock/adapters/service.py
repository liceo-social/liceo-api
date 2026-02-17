from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import Aggregate
from liceo.labs.db.core import AbstractService, managed_service, transactional
from ..application.service import EventStoreService
from ..application.repository import EventStoreRepository
from ..domain.errors import ConcurrentException


@dataclass
@managed_service
class DatabaseEventStoreService(EventStoreService, AbstractService):
    events: EventStoreRepository

    @transactional()
    def append(self, aggregate: Aggregate) -> None:
        if (self.events.append_batched_events(aggregate._events) != len(aggregate._events)):
            raise ConcurrentException()
