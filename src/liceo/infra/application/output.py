from abc import ABC
from shortuuid import uuid


class AbstractRepository(ABC):
    def generate_id(self) -> str:
        return uuid()
