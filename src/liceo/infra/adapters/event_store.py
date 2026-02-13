from liceo.infra.application.output import EventStore
from liceo.labs.sherlock.core import Aggregate, AggregateEvent
from liceo.labs.logs import logged


class ConsoleEventStore(EventStore, logged("liceo.infra.adapters.ConsoleEventStore")):
    def append(self, aggregate: Aggregate) -> None:
        for ev in aggregate._events:
            self.append_event(ev)

    def append_event(self, event: AggregateEvent) -> None:
        self._logger.info(f"Event stored: {event.event_type}")
