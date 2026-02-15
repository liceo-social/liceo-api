from abc import ABC, abstractmethod
from ..domain import entities


class EventStoreService(ABC):
    @abstractmethod
    def append_event(self, event: entities.AggregateEvent) -> None:
        pass

    @abstractmethod
    def append(self, aggregate: entities.Aggregate) -> None:
        pass
