from sqlalchemy import create_engine
from typing import Any, List, Mapping
from sqlalchemy import Connection as SAConnection, create_engine, text
from liceo.labs.db.core import Connection as LiceoConnection, ConnectionFactory as LiceoConnectionFactory
from liceo.labs.db.core import ExecutionParams


class SQLAlchemyConnection(LiceoConnection):
    def __init__(self, conn: SAConnection):
        self._conn = conn
        self._tx = conn.begin()

    def one(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, bool] | None = None) -> dict | None:
        sql = self._filter_parameters(sql, params=params)
        sql = self._filter_order_by(sql, orders=order_by)
        result = self._conn.execute(statement=text(sql), parameters=params)
        first_row = result.first()

        return dict(first_row._mapping) if first_row else None

    def insert(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        sql = self._filter_parameters(sql, params=params)
        return self.one(sql, params, order_by=None)

    def all(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, bool] | None = None) -> List[dict]:
        sql = self._filter_parameters(sql, params=params)
        sql = self._filter_order_by(sql, orders=order_by)
        print("==================>")
        print(sql)
        result = self._conn.execute(statement=text(sql), parameters=params)
        return [dict(one._mapping) for one in result.fetchall() if one]

    def execute(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, bool] | None = None) -> Any:
        sql = self._filter_parameters(sql, params=params)
        sql = self._filter_order_by(sql, orders=order_by)
        return self._conn.execute(statement=text(sql), parameters=params)

    def commit(self) -> None:
        if self._tx.is_active:
            self._tx.commit()

    def rollback(self) -> None:
        if self._tx.is_active:
            self._tx.rollback()

    def close(self) -> None:
        self._conn.close()


class SQLAlchemyConnectionFactory(LiceoConnectionFactory):
    def __init__(self, url: str):
        self._engine = create_engine(url)

    def create(self) -> LiceoConnection:
        sa_conn = self._engine.connect()
        return SQLAlchemyConnection(sa_conn)
