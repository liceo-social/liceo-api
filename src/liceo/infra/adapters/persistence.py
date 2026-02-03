from contextlib import contextmanager
from typing import Any, List

from sqlalchemy import Connection, Engine, create_engine, text

from liceo.infra.application.output import (
    TransactionalOutputPort,
    TransactionManager,
)
from liceo.labs.db.core import Connection as OptiakConnection
from liceo.labs.db.core import (
    ExecutionParams,
)


class DummyTransactional(TransactionalOutputPort):
    def __enter__(self):
        print("created transactional context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("transaction exited")

    def commit(self):
        print("transaction committed")

    def rollback(self):
        print("transaction did rollback")


class DummyTransactionalSupport(TransactionManager):
    def create(self) -> TransactionalOutputPort:
        return DummyTransactional()


class SQLAlchemyConnection(OptiakConnection):
    class TransactionalConnection(OptiakConnection):
        conn: Connection

        def __init__(self, conn: Connection):
            self.conn = conn

        def one(self, sql: str, params: ExecutionParams | None) -> dict | None:
            result = self.conn.execute(statement=text(sql), parameters=params)
            first_row = result.first()

            return dict(first_row._mapping) if first_row else None

        def insert(self, sql: str, params: ExecutionParams | None) -> dict | None:
            return self.one(sql, params)

        def all(self, sql: str, params: ExecutionParams | None) -> List[dict]:
            result = self.conn.execute(statement=text(sql), parameters=params)
            return [dict(one._mapping) for one in result.fetchall() if one]

        def execute(self, sql: str, params: ExecutionParams | None) -> Any:
            return self.conn.execute(statement=text(sql), parameters=params)

        @contextmanager
        def begin(self):
            yield self

    engine: Engine

    def __init__(self, url: str):
        self.engine = create_engine(url)

    def one(self, sql: str, params: ExecutionParams | None) -> dict | None:
        with self.engine.connect() as conn:
            result = conn.execute(statement=text(sql), parameters=params)
            first_row = result.first()

            return dict(first_row._mapping) if first_row else None

    def insert(self, sql: str, params: ExecutionParams | None) -> dict | None:
        return self.one(sql, params)

    def all(self, sql: str, params: ExecutionParams | None) -> List[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(statement=text(sql), parameters=params)
            first_row = result.first()

            if first_row:
                return [dict(one._mapping) for one in result.fetchall()]

            return []

    def execute(self, sql: str, params: ExecutionParams | None) -> Any:
        with self.engine.connect() as conn:
            return conn.execute(statement=text(sql), parameters=params)

    @contextmanager
    def begin(self):
        with self.engine.connect() as conn:
            with conn.begin():
                yield SQLAlchemyConnection.TransactionalConnection(conn)
