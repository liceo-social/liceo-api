from abc import ABC, abstractmethod
from liceo.security.permissions.domain import entities


class SavePermissionPort(ABC):
    @abstractmethod
    def save_permission(self, permission: entities.Permission) -> entities.Permission:
        pass


class SecurityPort(ABC):
    @abstractmethod
    def check_permissions(self, permissions: list[str], id: str):
        pass


class GenerateIdPort(ABC):
    @abstractmethod
    def next_id(self) -> str:
        pass
