from abc import ABC, abstractmethod
from ..domain import entities


class EventStoreService(ABC):
    @abstractmethod
    def append(self, aggregate: entities.Aggregate) -> None:
        pass
