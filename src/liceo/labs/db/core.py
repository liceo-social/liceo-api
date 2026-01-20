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
    @abstractmethod
    def one(self, sql: str, params: ExecutionParams | None) -> dict | None:
        pass

    @abstractmethod
    def insert(self, sql: str, params: ExecutionParams | None) -> dict | None:
        pass

    @abstractmethod
    def all(self, sql: str, params: ExecutionParams | None) -> List[dict]:
        pass

    @abstractmethod
    def execute(self, sql: str, params: ExecutionParams | None) -> Any:
        pass

    @abstractmethod
    def begin(self) -> _GeneratorContextManager["Connection", None, None]:
        pass


class Repository:
    def __init__(self, connection: Connection):
        self.connection = connection

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
