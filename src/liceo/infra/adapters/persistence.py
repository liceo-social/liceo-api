from dataclasses import dataclass
from sqlalchemy import create_engine
from typing import Any, List, Mapping
from liceo.labs.utils import singleton
from liceo.infra.domain.vo import DatabaseConfig
from sqlalchemy import Connection as SAConnection, create_engine, text
from liceo.labs.db.core import Connection as LiceoConnection, ConnectionFactory as LiceoConnectionFactory
from liceo.labs.db.core import ExecutionParams


class SQLAlchemyConnection(LiceoConnection):
    def __init__(self, conn: SAConnection):
        self._conn = conn

    def one(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        result = self._conn.execute(statement=text(sql), parameters=params)
        first_row = result.first()
        return dict(first_row._mapping) if first_row else None

    def insert(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        return self.one(sql, params)

    def all(self, sql: str, params: ExecutionParams | None = None) -> List[dict]:
        result = self._conn.execute(statement=text(sql), parameters=params)
        return [dict(one._mapping) for one in result.fetchall() if one]

    def execute(self, sql: str, params: ExecutionParams | None = None) -> Any:
        return self._conn.execute(statement=text(sql), parameters=params)

    def begin(self) -> None:
        self._conn.begin()

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def close(self) -> None:
        self._conn.close()

    def create_savepoint(self, name: str) -> None:
        self._conn.begin_nested()

    def rollback_to_savepoint(self, name: str) -> None:
        if self._conn.in_nested_transaction() and self._conn._nested_transaction:
            self._conn._nested_transaction.rollback()

    def release_savepoint(self, name: str) -> None:
        if self._conn.in_nested_transaction() and self._conn._nested_transaction:
            self._conn._nested_transaction.commit()


@singleton
class SQLAlchemyConnectionFactory(LiceoConnectionFactory):
    def __init__(self, database_config: DatabaseConfig):
        self._engine = create_engine(
            database_config.get_url(),
            pool_size=database_config.pool_size,
            pool_timeout=database_config.pool_timeout,
            max_overflow=database_config.max_overflow,
            pool_recycle=database_config.pool_recycle,
            pool_pre_ping=database_config.pool_pre_ping
        )

    def create(self) -> LiceoConnection:
        return SQLAlchemyConnection(self._engine.connect())
