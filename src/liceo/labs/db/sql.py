import os
import sys
import inspect
from functools import wraps, lru_cache
from logging import getLogger
from typing import Any, Callable, Mapping, Sequence, TypeVar, Union
from pathlib import Path
from liceo.labs.db.core import Repository

A = TypeVar("A", bound=Any)

logger = getLogger("poirot.core")

SingleParams = Mapping[str, Any]
MultiParams = Sequence[Mapping[str, Any]]
ExecutionParams = Union[SingleParams, MultiParams]

# to cache sql resolution in production
CACHE_SQL: bool = os.getenv("SHERLOCK_CACHE_SQL") is not None


class SQLResolver:
    @staticmethod
    def _resolve_sql_file_cacheable(module_name: str, func_name: str) -> str:
        logger.debug(
            "resolving sql file ['%s', '%s']",
            module_name,
            func_name
        )
        module = sys.modules.get(module_name)
        if module is None or not module.__file__:
            # module not loaded or invalid
            raise Exception(f"module {module_name} not loaded or invalid")

        module_path = Path(module.__file__).parent
        sql_path = module_path / "sql" / f"{func_name}.sql"

        if not sql_path.is_file():
            # SQL file does not exist
            raise Exception(f"SQL file {sql_path} does not exist")

        try:
            with open(sql_path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, IOError):
            # Could not read file for some reason
            raise Exception(f"Could not read file {sql_path} for some reason")

    @staticmethod
    @lru_cache(maxsize=None)
    def _resolve_sql_cached(module_name: str, func_name: str) -> str:
        return SQLResolver._resolve_sql_file_cacheable(module_name, func_name)

    @staticmethod
    def _resolve_sql_uncached(module_name: str, func_name: str) -> str:
        return SQLResolver._resolve_sql_file_cacheable(module_name, func_name)

    @staticmethod
    def resolve_sql(func: Callable[..., Any]) -> str:
        module_name = func.__module__
        func_name = func.__name__
        if CACHE_SQL:
            return SQLResolver._resolve_sql_cached(module_name, func_name)
        return SQLResolver._resolve_sql_uncached(module_name, func_name)


class SQLRepository(Repository):
    def resolve_sql(self, func: Callable[..., Any]) -> str:
        return SQLResolver.resolve_sql(func)

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
        @wraps(func)
        def wrapper(self: SQLRepository, *args: Any, **kwargs: Any) -> A:
            sql_content = self.resolve_sql(func)

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
                logger.debug(f"executing find___ query: {func.__name__}")
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
