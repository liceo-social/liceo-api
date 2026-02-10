from abc import ABC, abstractmethod
from typing import Iterator


class Storage(ABC):
    @abstractmethod
    def write(self, key: str, data: Iterator[bytes]) -> str:
        pass

    @abstractmethod
    def read(
        self,
        key: str,
        chunk_size: int = 1024 * 1024,
    ) -> Iterator[bytes]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass
