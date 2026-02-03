from liceo.infra.application.output import EventStore
from liceo.labs.sherlock.core import Aggregate, AggregateEvent


class ConsoleEventStore(EventStore):
    def append(self, aggregate: Aggregate) -> None:
        for ev in aggregate._events:
            print(ev)

    def append_event(self, event: AggregateEvent) -> None:
        print(event)
