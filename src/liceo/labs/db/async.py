
from dataclasses import dataclass
from contextlib import asynccontextmanager
from itertools import count
from contextvars import ContextVar
from contextlib import AbstractAsyncContextManager
from typing import Optional
from abc import ABC, abstractmethod


class AsyncConnection(ABC):
    @abstractmethod
    async def begin(self) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def create_savepoint(self, name: str) -> None: ...

    @abstractmethod
    async def rollback_to_savepoint(self, name: str) -> None: ...

    @abstractmethod
    async def release_savepoint(self, name: str) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


class AsyncConnectionFactory(ABC):
    @abstractmethod
    async def create(self) -> AsyncConnection:
        pass


_current_async_connection: ContextVar[AsyncConnection | None] = ContextVar(
    "_current_async_connection",
    default=None,
)

_async_transaction_depth: ContextVar[int] = ContextVar(
    "_async_transaction_depth",
    default=0,
)


class AsyncConnectionManager(AbstractAsyncContextManager):
    def __init__(self, factory: AsyncConnectionFactory):
        self._factory = factory
        self._conn: Optional[AsyncConnection] = None
        self._owns_connection = False
        self._token = None

    async def __aenter__(self):
        conn = _current_async_connection.get()

        if conn is None:
            self._conn = await self._factory.create()
            self._owns_connection = True
            self._token = _current_async_connection.set(self._conn)
        else:
            self._conn = conn

        return self._conn

    async def __aexit__(self, exc_type, exc, tb):
        if self._owns_connection:
            if self._token:
                _current_async_connection.reset(self._token)
            if self._conn is not None:
                await self._conn.close()


_async_savepoint_counter = count()


class AsyncTransactionManager(AbstractAsyncContextManager):
    def __init__(self, factory: AsyncConnectionFactory):
        self._factory = factory
        self._conn: AsyncConnection | None = None
        self._owns_connection = False
        self._savepoint: str | None = None
        self._token = None

    async def __aenter__(self):
        conn = _current_async_connection.get()

        # ---- connection ownership ------------------------------
        if conn is None:
            self._conn = await self._factory.create()
            self._owns_connection = True
            self._token = _current_async_connection.set(self._conn)
        else:
            self._conn = conn

        # ---- transaction ownership -----------------------------
        depth = _async_transaction_depth.get()

        if depth == 0:
            await self._conn.begin()
        else:
            self._savepoint = f"sp_{next(_async_savepoint_counter)}"
            await self._conn.create_savepoint(self._savepoint)

        _async_transaction_depth.set(depth + 1)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        depth = _async_transaction_depth.get() - 1
        _async_transaction_depth.set(depth)

        if self._conn is None:
            raise Exception("Transaction connection closed unexpectedly")

        try:
            if exc_type:
                if depth == 0:
                    await self._conn.rollback()
                elif self._savepoint:
                    await self._conn.rollback_to_savepoint(self._savepoint)
            else:
                if depth == 0:
                    await self._conn.commit()
                elif self._savepoint:
                    await self._conn.release_savepoint(self._savepoint)
        finally:
            if self._owns_connection:
                if self._token:
                    _current_async_connection.reset(self._token)
                await self._conn.close()


class AsyncRepository:
    def __init__(self, factory: AsyncConnectionFactory):
        self._factory = factory

    @asynccontextmanager
    async def _connection_scope(self):
        conn = _current_async_connection.get()

        if conn is not None:
            yield conn
            return

        conn = await self._factory.create()
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.close()


@dataclass
class AsyncAbstractService:
    connection_manager: AsyncConnectionManager
    transaction_manager: AsyncTransactionManager

    @property
    def connection(self) -> AsyncConnection | None:
        return _current_async_connection.get()

    def transactional(self):
        return self.transaction_manager

    def connectional(self):
        return self.connection_manager
