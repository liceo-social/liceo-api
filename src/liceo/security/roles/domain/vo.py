from datetime import datetime
from dataclasses import dataclass

from typing import Generic, TypeVar


@dataclass(frozen=True)
class PermissionId:
    id: str


@dataclass
class UserId:
    id: str


@dataclass
class RoleId:
    id: str


T = TypeVar("T")
