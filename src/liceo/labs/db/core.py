from functools import wraps
from dataclasses import dataclass
from contextlib import AbstractContextManager, contextmanager
from contextvars import ContextVar
from typing import Optional, Any
from abc import ABC, abstractmethod
from typing import Any, List, Mapping, Sequence, Union
from liceo.labs.logs import logged

SingleParams = Mapping[str, Any]
MultiParams = Sequence[Mapping[str, Any]]
ExecutionParams = Union[SingleParams, MultiParams]


class Connection(ABC):
    @abstractmethod
    def one(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        pass

    @abstractmethod
    def insert(self, sql: str, params: ExecutionParams | None = None) -> dict | None:
        pass

    @abstractmethod
    def all(self, sql: str, params: ExecutionParams | None = None) -> List[dict]:
        pass

    @abstractmethod
    def execute(self, sql: str, params: ExecutionParams | None = None) -> Any:
        pass

    @abstractmethod
    def begin(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def create_savepoint(self, name: str) -> None:
        pass

    @abstractmethod
    def rollback_to_savepoint(self, name: str) -> None:
        pass

    @abstractmethod
    def release_savepoint(self, name: str) -> None:
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

_transaction_depth: ContextVar[int] = ContextVar(
    "_transaction_depth",
    default=0,
)


class ConnectionManager(AbstractContextManager, logged("liceo.db.core.ConnectionManager")):
    """
    Ambient connection scope without transaction semantics.
    """

    def __init__(self, factory: ConnectionFactory):
        self._factory = factory
        self._conn: Optional[Connection] = None
        self._owns_connection = False
        self._token = None

    def __enter__(self):
        self._conn = _current_connection.get()
        self._logger.debug("CM-getting-connection")
        if self._conn is None:
            self._logger.debug("CM-created-connection")
            self._conn = self._factory.create()
            self._owns_connection = True
            self._token = _current_connection.set(self._conn)

        return self._conn

    def __exit__(self, exc_type, exc, tb):
        if self._owns_connection:
            if self._token:
                _current_connection.reset(self._token)
            if self._conn is not None:
                self._logger.debug("CM-closing-connection")
                self._conn.close()


class TransactionManager:
    def __init__(self, connection_factory: ConnectionFactory):
        self._factory = connection_factory
        self._conn = None
        self._conn_token = None
        self._depth_token = None
        self._owns_connection = False
        self._savepoint_name = None

    def __enter__(self):
        conn = _current_connection.get()
        depth = _transaction_depth.get()

        # Ensure connection exists
        if conn is None:
            self._conn = self._factory.create()
            self._owns_connection = True
            self._conn_token = _current_connection.set(self._conn)
        else:
            self._conn = conn

        if depth == 0:
            self._conn.begin()
        else:
            self._conn.create_savepoint(f"sp_{depth}")

        # Increase depth
        self._depth_token = _transaction_depth.set(depth + 1)

        return self._conn

    def __exit__(self, exc_type, exc, tb):
        depth = _transaction_depth.get() - 1

        try:
            if self._conn:
                if exc_type is None:
                    if depth == 0:
                        self._conn.commit()
                    elif self._savepoint_name:
                        self._conn.release_savepoint(self._savepoint_name)
                else:
                    if depth == 0:
                        self._conn.rollback()
                    elif self._savepoint_name:
                        self._conn.rollback_to_savepoint(self._savepoint_name)
        finally:
            if self._depth_token:
                _transaction_depth.reset(self._depth_token)

            if self._owns_connection:
                if self._conn_token:
                    _current_connection.reset(self._conn_token)
                    if self._conn:
                        self._conn.close()


class Repository:
    def __init__(self, factory: ConnectionFactory):
        self._factory = factory

    def _get_connection(self) -> Connection:
        conn = _current_connection.get()
        if conn is not None:
            return conn

        # fallback: autonomous connection
        return self._factory.create()

    @contextmanager
    def _connection_scope(self):
        conn = _current_connection.get()

        if conn is not None:
            yield conn
            return

        conn = self._factory.create()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class ConnectionManagerFactory:
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def __call__(self):
        return ConnectionManager(self._connection_factory)


class TransactionManagerFactory:

    def __init__(self, connection_factory):
        self._connection_factory = connection_factory

    def __call__(self):
        return TransactionManager(self._connection_factory)


@dataclass
class AbstractService:
    connection_manager_factory: ConnectionManagerFactory
    transaction_manager_factory: TransactionManagerFactory

    @property
    def connection(self) -> Connection | None:
        """
        Exposes the ambient connection for advanced cases.
        Prefer repositories instead.
        """
        return _current_connection.get()

    def transactional(self):
        return self.transaction_manager_factory

    def connectional(self):
        return self.connection_manager_factory


def managed_service(cls):
    """
    Wrap all public methods of the class to execute inside
    `self.connection_manager` by default.
    """
    for attr_name, attr in vars(cls).items():
        if attr_name.startswith("_") or not callable(attr):
            continue
        if getattr(attr, "_skip_default_connection", False):
            continue
        setattr(cls, attr_name, _wrap_with_connection(attr))
    return cls


def _wrap_with_connection(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        with self.connection_manager_factory():
            return fn(self, *args, **kwargs)
    return wrapper


def skip_default_connection(fn):
    fn._skip_default_connection = True
    return fn


def transactional():
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            with self.transaction_manager_factory():
                return fn(self, *args, **kwargs)
        return wrapper
    return decorator
