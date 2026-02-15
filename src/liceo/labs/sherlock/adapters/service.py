from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import Aggregate, AggregateEvent
from liceo.labs.db.core import AbstractService, managed_service, transactional
from ..application.service import EventStoreService
from ..application.repository import EventStoreRepository


@dataclass
@managed_service
class DatabaseEventStoreService(EventStoreService, AbstractService):
    events: EventStoreRepository

    @transactional()
    def append(self, aggregate: Aggregate) -> None:
        for event in aggregate._events:
            self.append_event(event)

    def append_event(self, event: AggregateEvent) -> None:
        self.events.append_event(event)
