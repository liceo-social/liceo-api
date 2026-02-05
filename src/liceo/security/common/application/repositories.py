from abc import ABC, abstractmethod


class PermissionsRepository(ABC):
    @abstractmethod
    def find_all_roles_by_permission_name(self, name: str) -> list[str]:
        pass
