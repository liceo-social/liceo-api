import os
from typing import Iterator
from dataclasses import dataclass
from liceo.infra.domain.vo import FileConfig
from ..application.storage import Storage


@dataclass
class LocalStorage(Storage):
    configuration: FileConfig

    def _path(self, key: str) -> str:
        return os.path.join(self.configuration.root_path, key)

    def write(self, key: str, data: Iterator[bytes]) -> str:
        path = self._path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            for chunk in data:
                f.write(chunk)

        return path

    def read(
        self,
        key: str,
        chunk_size: int = 1024 * 1024,
    ) -> Iterator[bytes]:
        with open(self._path(key), "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    def delete(self, key: str) -> None:
        os.remove(self._path(key))
