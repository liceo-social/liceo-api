import json
from shortuuid import uuid
from dataclasses import dataclass
from liceo.labs.logs import logged
from ..application.service import EventStoreService
from ..domain.entities import Aggregate, AggregateEvent


@dataclass
class ConsoleEventStore(EventStoreService, logged("liceo.infra.adapters.ConsoleEventStore")):
    def append(self, aggregate: Aggregate) -> None:
        for ev in aggregate._events:
            self.append_event(ev)

    def append_event(self, event: AggregateEvent) -> None:
        self._logger.info(
            f"Event stored: {event.aggregate_type} | {event.event_type} | {event.version} | {event.aggregate_id} | {uuid()} | {json.dumps(event.unsecure_dict())}")
