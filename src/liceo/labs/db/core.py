from typing import Optional
from contextlib import AbstractContextManager
from contextvars import ContextVar
import inspect
from abc import ABC, abstractmethod
from contextlib import _GeneratorContextManager
from pathlib import Path
from typing import Any, Callable, List, Mapping, Sequence, TypeVar, Union

A = TypeVar("A", bound=Any)

SingleParams = Mapping[str, Any]
MultiParams = Sequence[Mapping[str, Any]]
ExecutionParams = Union[SingleParams, MultiParams]


class Connection(ABC):
    def _filter_parameters(self, sql: str, params: ExecutionParams | None) -> str:
        if params is None:
            return sql

        keys = []
        lines = []

        if isinstance(params, Mapping):
            keys = params.keys()

        if isinstance(params, Sequence):
            if all([isinstance(param, Mapping) for param in params]):
                keys = set([x for x in [p.keys() for p in params]])

        sql_keys = [f":{k}" for k in keys]

        for line in sql.splitlines():
            if line.__contains__(':'):
                if any([line.__contains__(k) for k in sql_keys]):
                    lines.append(line)
            else:
                lines.append(line)

        return "\n".join(lines)

    def _filter_order_by(self, sql: str, orders: Mapping[str, bool] | None) -> str:
        if orders is None or len(orders) <= 0:
            return sql

        lines = []
        for line in sql.splitlines():
            if line.lower().__contains__("order by"):
                orders_str = ",".join(
                    [f"{k} {'ASC' if v else 'DESC'}" for k, v in orders.items()])
                lines.append(f"ORDER BY {orders_str}")
            else:
                lines.append(line)

        return "\n".join(lines)

    @abstractmethod
    def one(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, Any] | None = None) -> dict | None:
        pass

    @abstractmethod
    def insert(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        pass

    @abstractmethod
    def all(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, Any] | None = None) -> List[dict]:
        pass

    @abstractmethod
    def execute(self, sql: str, params: ExecutionParams | None = None, order_by: Mapping[str, Any] | None = None) -> Any:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class ConnectionFactory(ABC):
    @abstractmethod
    def create(self) -> Connection:
        pass


_current_connection: ContextVar[Connection | None] = ContextVar(
    "_current_connection",
    default=None,
)


class Repository:
    def __init__(self, factory: ConnectionFactory):
        self._factory = factory

    def _get_connection(self) -> Connection:
        conn = _current_connection.get()
        if conn is not None:
            return conn

        # fallback: autonomous connection
        return self._factory.create()

    def resolve_sql_file(self, func: Callable[..., Any]) -> Path:
        sql_dir = Path(inspect.getfile(func)).parent / "sql"

        module = inspect.getmodule(func)
        if module:
            sql_dir = Path(inspect.getfile(module)).parent / "sql"

        sql_filename = "{}.sql".format(func.__name__)
        return sql_dir / sql_filename

    def resolve_sql(self, func: Callable[..., Any]) -> str:
        with open(self.resolve_sql_file(func), "r") as file:
            return file.read()


class Transaction(AbstractContextManager):
    def __init__(self, factory: ConnectionFactory):
        self._factory = factory
        self._connection: Connection
        self._token = None

    def __enter__(self):
        self._connection = self._factory.create()
        self._token = _current_connection.set(self._connection)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self._connection.commit()
            else:
                self._connection.rollback()
        finally:
            if self._token is not None:
                _current_connection.reset(self._token)
            self._connection.close()
