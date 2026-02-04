from abc import ABC, abstractmethod


class HashPassword(ABC):
    @abstractmethod
    def hash_passw(self, pwd) -> str:
        pass


class CheckUserPermissions(ABC):
    @abstractmethod
    def check_permissions(self, permissions: list[str], user_id: str) -> bool:
        pass


class GenerateToken(ABC):
    @abstractmethod
    def generate_token(self, username: str) -> str:
        pass
