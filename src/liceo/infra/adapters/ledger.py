from typing import TypeVar

from liceo.infra.application.output import LedgerPort
from liceo.labs.sherlock.core import Aggregate, AggregateEvent


class ConsoleLedger(LedgerPort):
    def persist(self, aggregate: Aggregate) -> None:
        for ev in aggregate._events:
            print(ev)

    def persist_event(self, event: AggregateEvent) -> None:
        print(event)
