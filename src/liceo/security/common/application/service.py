from abc import ABC, abstractmethod


class SecurityService(ABC):
    @abstractmethod
    def hash_passw(self, pwd) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        pass

    @abstractmethod
    def check_permission_in_roles(self, permission: str, roles: list[str]) -> bool:
        pass

    @abstractmethod
    def generate_token(self, id: str, roles: list[str]) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass
