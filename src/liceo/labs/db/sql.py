import functools
import inspect
from logging import getLogger
from typing import Any, Callable, Mapping, Sequence, TypeVar, Union
from pathlib import Path
from liceo.labs.db.core import Repository

A = TypeVar("A", bound=Any)

logger = getLogger("poirot.core")

SingleParams = Mapping[str, Any]
MultiParams = Sequence[Mapping[str, Any]]
ExecutionParams = Union[SingleParams, MultiParams]


class SQLRepository(Repository):
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

    def sql_optimize(self, sql, params: ExecutionParams | None, orders: Mapping[str, bool] | None) -> str:
        return self.sql_optimize_order_by(self.sql_optimize_params(sql, params), orders)

    def sql_optimize_params(self, sql: str, params: ExecutionParams | None) -> str:
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
                # if there's any parameter present
                if any([line.__contains__(k) for k in sql_keys]):
                    lines.append(line)
                # if not only if there're expressions like ::text[]
                elif line.__contains__('::'):
                    lines.append(line)
            else:
                lines.append(line)

        return "\n".join(lines)

    def sql_optimize_order_by(self, sql: str, orders: Mapping[str, bool] | None) -> str:
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


def sql(mapper: Callable[..., A] = lambda row: row):
    def decorator(func: Callable[..., Any]) -> Callable[..., A]:
        @functools.wraps(func)
        def wrapper(self: SQLRepository, *args: Any, **kwargs: Any) -> A:
            sql_file = self.resolve_sql_file(func)
            sql_content = ""

            if not sql_file.exists():
                raise Exception("SQL file not found!")

            with sql_file.open() as file_content:
                sql_content = "\n".join(file_content.readlines())

            if not sql_content:
                raise Exception("No SQL content found in file!")

            if kwargs and len(args) > 0:
                raise Exception("Can't decide whether we should use args or kwargs!")

            if kwargs:
                logger.debug("kwargs {}".format(str(kwargs)))

            if len(args) > 0:
                sql_args = inspect.getfullargspec(func).args
                sql_args.remove("self")
                kwargs = {next[0]: next[1] for next in zip(sql_args, args)}

            if func.__name__.startswith("find_all_"):
                logger.debug("executing find_all___ query")
                all = self._get_connection().all(sql=sql_content, params=kwargs)
                return mapper([next for next in all])

            if func.__name__.startswith("paged_"):
                logger.debug("executing paged___ query")
                all = self._get_connection().all(sql=sql_content, params=kwargs)
                return mapper(all)

            if func.__name__.startswith("find_") or func.__name__.startswith("insert_"):
                logger.debug("executing find___ query")
                one = self._get_connection().one(sql=sql_content, params=kwargs)
                return mapper(one)

            if func.__name__.startswith("is_"):
                logger.debug("executing is___ query")
                one = self._get_connection().one(sql=sql_content, params=kwargs)
                return mapper(one)

            logger.debug("executing execute___ query")
            return self._get_connection().execute(sql=sql_content, params=kwargs)

        return wrapper

    return decorator
