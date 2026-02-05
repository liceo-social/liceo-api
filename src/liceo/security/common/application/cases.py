from abc import ABC, abstractmethod


class HashPassword(ABC):
    @abstractmethod
    def hash_passw(self, pwd) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        pass


class CheckPermissions(ABC):
    @abstractmethod
    def check_permission_in_roles(self, permission: str, roles: list[str]) -> bool:
        pass


class GenerateToken(ABC):
    @abstractmethod
    def generate_token(self, username: str, roles: list[str]) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass
