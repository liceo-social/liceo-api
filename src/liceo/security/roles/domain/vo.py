from datetime import datetime
from dataclasses import dataclass

from typing import TypeVar
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass(frozen=True)
class PermissionId:
    id: str


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class RoleId(AggregateId):
    id: str


T = TypeVar("T")
