from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, List, Self, TypeVar

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Sensitive(Generic[T]):
    value: T


@dataclass(kw_only=True)
class AggregateEvent(Generic[T, U], ABC):
    id: str = ""
    aggregate_id: str = ""
    aggregate_type: str = ""
    event_type: str
    event_at: datetime = datetime.now()
    event_by: U
    version: int = 0

    @abstractmethod
    def handle(self, aggregate: T) -> None:
        pass

    def unsecure_dict(self):
        unsecured = {}
        filtered = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ["id", "aggregate_type", "aggregate_id", "event_type", "version"]
        }
        for k, v in filtered.items():
            if type(v) is Sensitive:
                unsecured.update({k: v.value})
            else:
                unsecured.update({k: str(v)})

        return unsecured


class AggregateId:
    id: str

    def __str__(self) -> str:
        return self.id


ID = TypeVar("ID", bound=AggregateId)


@dataclass
class Aggregate(Generic[ID, U]):
    id: ID
    _version: int = field(default=0)
    _events: List[AggregateEvent[Self, U]] = field(default_factory=list)

    def append(self, event: AggregateEvent[Self, U]):
        if not self.id:
            raise Exception("Can't add without aggregate id")

        event.aggregate_id = self.id.id
        event.aggregate_type = self.aggregate_type
        event.handle(self)
        event.version = self._version + 1
        self._version += 1
        self._events.append(event)
        return self

    def check_version_matches(self, expected_version: int) -> bool:
        return self._version == expected_version

    @property
    @abstractmethod
    def aggregate_type(self) -> str:
        pass


@dataclass
class AggregateRoot(Aggregate[ID, U]):
    def append_child_aggregate_events(self, aggregate: Aggregate):
        for ev in self._events:
            self._events.append(ev)
        return self
