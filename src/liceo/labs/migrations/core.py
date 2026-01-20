from dataclasses import dataclass
from hashlib import sha256
from io import BufferedReader
from pathlib import Path
from typing import List, Self

from liceo.labs.db.core import Connection, Repository
from liceo.labs.logs import logged


class DBM(Repository, logged("optiak.labs.migrations")):
    @dataclass
    class FileContent:
        sql: str
        hash: str

    h256 = sha256()
    path: Path
    destroy_path: Path

    def __init__(
        self,
        connection: Connection,
        path: Path = Path("migrations"),
        destroy_path: Path = Path("destroy"),
    ):
        super().__init__(connection)
        self.path = path
        self.destroy_path = destroy_path

    def create_db(self) -> Self:
        MIGRATIONS_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL,
            name TEXT,
            applied_at timestamp,
            hash VARCHAR(256),
            UNIQUE(name)
        );
        """
        self.connection.execute(MIGRATIONS_TABLE_SQL, {})
        self._logger.info("migrations table created")
        return self

    def drop_db(self):
        MIGRATIONS_TABLE_DROP_SQL = """
        DROP TABLE migrations;
        """
        self.connection.execute(MIGRATIONS_TABLE_DROP_SQL, {})
        self._logger.info("migrations table deleted")

    def hash_file(self, content: bytes):
        """
        https://gist.github.com/jakekara/078899caaf8d5e6c74ef58d16ce7e703
        """
        # Read the contents of the file into the hash algorithm
        self.h256.update(content)

        # Print the digest/hash of the file's contents
        return self.h256.hexdigest()

    def _read_sql_files_from_path(self, path: Path) -> List[Path]:
        return [f.absolute() for f in path.iterdir() if f.is_file()]

    def _extract_file_content(self, file: BufferedReader) -> FileContent:
        file_bytes = file.read()
        file_hash = self.hash_file(file_bytes)
        return DBM.FileContent(sql=file_bytes.decode("utf-8"), hash=file_hash)

    def apply_migrations(self):
        ADD_MIGRATION_ENTRY = """
        INSERT INTO migrations (name, applied_at, hash)
        VALUES (:filename, now(), :hash)
        ON CONFLICT DO NOTHING;
        """
        for filename in self._read_sql_files_from_path(self.path):
            with open(filename, "rb") as file:
                file_content = self._extract_file_content(file)
                # running migration
                self.connection.execute(
                    ADD_MIGRATION_ENTRY,
                    {"filename": filename.name, "hash": file_content.hash},
                )
                self.connection.execute(file_content.sql, {})
                self._logger.info("migration %s applied", filename.name)

    def truncate_all(self):
        for filename in self._read_sql_files_from_path(self.destroy_path):
            with open(filename, "rb") as file:
                self.connection.execute(self._extract_file_content(file).sql, {})
                self._logger.info("truncate all file '%s' applied", filename.name)
