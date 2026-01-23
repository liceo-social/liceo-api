from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from liceo.infra.domain.vo import Pagination, Paged
from liceo.security.permissions.domain import entities


T = TypeVar("T")


class SavePermissionPort(ABC):
    @abstractmethod
    def save_permission(self, permission: entities.Permission) -> entities.Permission:
        pass


class ListPermissionsPort(ABC):
    @abstractmethod
    def list_permissions(self, pagination: Pagination) -> Paged[entities.Permission]:
        pass


class SecurityPort(ABC):
    @abstractmethod
    def check_permissions(self, permissions: list[str], id: str):
        pass


class GenerateIdPort(ABC):
    @abstractmethod
    def next_id(self) -> str:
        pass
