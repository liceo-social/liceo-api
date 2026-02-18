from datetime import datetime
from dataclasses import dataclass

from typing import TypeVar
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass(frozen=True)
class PermissionId:
    id: str

    def __str__(self) -> str:
        return self.id


@dataclass
class UserId(AggregateId):
    id: str

    def __str__(self) -> str:
        return self.id


@dataclass
class RoleId(AggregateId):
    id: str

    def __str__(self) -> str:
        return self.id


T = TypeVar("T")
